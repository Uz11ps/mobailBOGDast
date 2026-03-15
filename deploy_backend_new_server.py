import os
import posixpath
import paramiko

HOST = "194.67.99.161"
USER = "root"
PASSWORD = "BfiR0QRRjX7NDI7A"

PROJECT_ROOT = r"c:\Users\1\Desktop\cursor\Pojertovania_mobail"
LOCAL_BACKEND = r"c:\Users\1\Desktop\cursor\Pojertovania_mobail\backend"
LOCAL_USER_PANEL = r"c:\Users\1\Desktop\cursor\Pojertovania_mobail\user_panel"
LOCAL_ADMIN_PANEL = r"c:\Users\1\Desktop\cursor\Pojertovania_mobail\admin_panel"
LOCAL_IMG = r"c:\Users\1\Desktop\cursor\Pojertovania_mobail\img"

REMOTE_ROOT = "/root/mobailBOGDast"
REMOTE_BACKEND = f"{REMOTE_ROOT}/backend"
REMOTE_WEB_ROOT = "/var/www/charity_web"

EXCLUDE_DIRS = {"node_modules", "dist", ".git", ".dart_tool"}
EXCLUDE_FILES = {".DS_Store"}
MEDIA_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def run(ssh: paramiko.SSHClient, cmd: str, check: bool = True):
    print(f"\n>>> {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    code = stdout.channel.recv_exit_status()
    out = stdout.read().decode("utf-8", "ignore")
    err = stderr.read().decode("utf-8", "ignore")
    if out.strip():
        print(out.strip().encode("cp1252", errors="replace").decode("cp1252"))
    if err.strip():
        print(err.strip().encode("cp1252", errors="replace").decode("cp1252"))
    if check and code != 0:
        raise RuntimeError(f"Command failed ({code}): {cmd}")
    return code, out, err


def sftp_mkdir_p(sftp: paramiko.SFTPClient, remote_dir: str):
    parts = []
    cur = remote_dir
    while cur not in ("", "/"):
        parts.append(cur)
        cur = posixpath.dirname(cur)

    for directory in reversed(parts):
        try:
            sftp.stat(directory)
        except FileNotFoundError:
            sftp.mkdir(directory)


def upload_dir(sftp: paramiko.SFTPClient, local_dir: str, remote_dir: str):
    sftp_mkdir_p(sftp, remote_dir)

    for root, dirs, files in os.walk(local_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        rel = os.path.relpath(root, local_dir)
        rel_posix = "" if rel == "." else rel.replace("\\", "/")
        target_dir = remote_dir if not rel_posix else posixpath.join(remote_dir, rel_posix)
        sftp_mkdir_p(sftp, target_dir)

        for filename in files:
            if filename in EXCLUDE_FILES:
                continue
            local_path = os.path.join(root, filename)
            remote_path = posixpath.join(target_dir, filename)
            sftp.put(local_path, remote_path)


def upload_media_files(sftp: paramiko.SFTPClient, local_dir: str, remote_dir: str):
    if not os.path.isdir(local_dir):
        return

    sftp_mkdir_p(sftp, remote_dir)
    for filename in os.listdir(local_dir):
        local_path = os.path.join(local_dir, filename)
        if not os.path.isfile(local_path):
            continue
        ext = os.path.splitext(filename)[1].lower()
        if ext not in MEDIA_EXTENSIONS:
            continue
        remote_path = posixpath.join(remote_dir, filename)
        sftp.put(local_path, remote_path)


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PASSWORD, timeout=30)

    try:
        run(ssh, "export DEBIAN_FRONTEND=noninteractive && apt-get update -y")
        run(
            ssh,
            "export DEBIAN_FRONTEND=noninteractive && "
            "apt-get install -y curl ca-certificates gnupg lsb-release software-properties-common",
        )
        run(
            ssh,
            "if ! command -v node >/dev/null 2>&1; then "
            "curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && "
            "apt-get install -y nodejs; "
            "fi",
        )
        run(ssh, "if ! command -v pm2 >/dev/null 2>&1; then npm i -g pm2; fi")
        run(ssh, "export DEBIAN_FRONTEND=noninteractive && apt-get install -y postgresql postgresql-contrib")
        run(ssh, "systemctl enable postgresql || true && systemctl start postgresql || true")
        run(ssh, "export DEBIAN_FRONTEND=noninteractive && apt-get install -y nginx")

        run(ssh, f"mkdir -p {REMOTE_BACKEND}")
        run(ssh, f"mkdir -p {REMOTE_WEB_ROOT}/user_panel {REMOTE_WEB_ROOT}/admin {REMOTE_WEB_ROOT}/uploads {REMOTE_WEB_ROOT}/assets")
        sftp = ssh.open_sftp()
        upload_dir(sftp, LOCAL_BACKEND, REMOTE_BACKEND)
        upload_dir(sftp, LOCAL_USER_PANEL, f"{REMOTE_WEB_ROOT}/user_panel")
        upload_dir(sftp, LOCAL_ADMIN_PANEL, f"{REMOTE_WEB_ROOT}/admin")
        upload_media_files(sftp, LOCAL_IMG, f"{REMOTE_WEB_ROOT}/uploads")
        if os.path.exists(os.path.join(LOCAL_USER_PANEL, "index.html")):
            sftp.put(os.path.join(LOCAL_USER_PANEL, "index.html"), f"{REMOTE_WEB_ROOT}/index.html")
        sftp.close()
        print("\n>>> backend + web files uploaded")

        db_password = "CharityStrongPass_2026!"
        run(
            ssh,
            "sudo -u postgres psql -tc \"SELECT 1 FROM pg_roles WHERE rolname='charity_user'\" "
            "| tr -d '[:space:]' | grep -q 1 || "
            f"sudo -u postgres psql -c \"CREATE USER charity_user WITH PASSWORD '{db_password}';\"",
        )
        run(
            ssh,
            "sudo -u postgres psql -tc \"SELECT 1 FROM pg_database WHERE datname='charity_db'\" "
            "| tr -d '[:space:]' | grep -q 1 || "
            "sudo -u postgres psql -c \"CREATE DATABASE charity_db OWNER charity_user;\"",
        )

        env_content = """PORT=3000
DB_HOST=127.0.0.1
DB_PORT=5432
DB_USERNAME=charity_user
DB_PASSWORD=CharityStrongPass_2026!
DB_NAME=charity_db
JWT_SECRET=NovaiaZhizn_JWT_2026_secure
"""
        run(ssh, f"cat > {REMOTE_BACKEND}/.env << 'EOF'\n{env_content}EOF")

        run(ssh, f"cd {REMOTE_BACKEND} && npm install")
        run(ssh, f"cd {REMOTE_BACKEND} && npm run build")
        run(
            ssh,
            f"cd {REMOTE_BACKEND} && "
            "(pm2 describe charity-api >/dev/null 2>&1 && pm2 restart charity-api || "
            "pm2 start dist/index.js --name charity-api)",
        )
        run(ssh, "pm2 save")
        run(ssh, "pm2 startup systemd -u root --hp /root || true")

        nginx_config = f"""server {{
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    root {REMOTE_WEB_ROOT};
    index index.html;

    location /api/ {{
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}

    location /uploads/ {{
        alias {REMOTE_WEB_ROOT}/uploads/;
        access_log off;
        expires 7d;
    }}

    location /admin/ {{
        alias {REMOTE_WEB_ROOT}/admin/;
        index dashboard.html;
        try_files $uri $uri/ /admin/dashboard.html;
    }}

    location / {{
        try_files $uri $uri/ /index.html;
    }}
}}
"""
        run(ssh, "rm -f /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default || true")
        run(ssh, "cat > /etc/nginx/sites-available/charity_web << 'EOF'\n" + nginx_config + "EOF")
        run(ssh, "ln -sfn /etc/nginx/sites-available/charity_web /etc/nginx/sites-enabled/charity_web")
        run(ssh, "nginx -t")
        run(ssh, "systemctl enable nginx || true && systemctl restart nginx")
        run(ssh, f"chown -R www-data:www-data {REMOTE_WEB_ROOT}")
        run(ssh, f"find {REMOTE_WEB_ROOT} -type d -exec chmod 755 {{}} \\;")
        run(ssh, f"find {REMOTE_WEB_ROOT} -type f -exec chmod 644 {{}} \\;")

        run(ssh, "pm2 status")
        run(ssh, "curl -sS http://127.0.0.1:3000/ || true")
        run(ssh, "curl -sS http://127.0.0.1:3000/api/collections || true")
        run(ssh, "curl -sS -I http://127.0.0.1/api/collections || true")
        run(ssh, "curl -sS -I http://127.0.0.1/ || true")
    finally:
        ssh.close()

    print("\nDONE")


if __name__ == "__main__":
    main()
