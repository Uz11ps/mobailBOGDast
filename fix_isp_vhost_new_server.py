import paramiko

HOST = "194.67.99.161"
USER = "root"
PASSWORD = "BfiR0QRRjX7NDI7A"

VHOST_PATH = "/etc/nginx/vhosts/www-root/194-67-99-161.regru.cloud.conf"
WEB_ROOT = "/var/www/charity_web"


def run(client: paramiko.SSHClient, cmd: str):
    print(f"\n>>> {cmd}")
    stdin, stdout, stderr = client.exec_command(cmd)
    code = stdout.channel.recv_exit_status()
    out = stdout.read().decode("utf-8", "ignore")
    err = stderr.read().decode("utf-8", "ignore")
    if out.strip():
        print(out.encode("cp1252", errors="replace").decode("cp1252"))
    if err.strip():
        print(err.encode("cp1252", errors="replace").decode("cp1252"))
    if code != 0:
        raise RuntimeError(f"Command failed ({code}): {cmd}")


def main():
    nginx_conf = f"""server {{
    server_name 194-67-99-161.regru.cloud www.194-67-99-161.regru.cloud 194.67.99.161;
    charset off;
    index index.html;
    root {WEB_ROOT};
    disable_symlinks if_not_owner from=$root_path;
    set $root_path {WEB_ROOT};
    access_log /var/www/httpd-logs/194-67-99-161.regru.cloud.access.log;
    error_log /var/www/httpd-logs/194-67-99-161.regru.cloud.error.log notice;
    listen 192.168.0.186:80 default_server;

    location /api/ {{
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}

    location /uploads/ {{
        alias {WEB_ROOT}/uploads/;
        access_log off;
        expires 7d;
    }}

    location /admin/ {{
        alias {WEB_ROOT}/admin/;
        index dashboard.html;
        try_files $uri $uri/ /admin/dashboard.html;
    }}

    location / {{
        try_files $uri $uri/ /index.html;
    }}
}}

server {{
    server_name 194-67-99-161.regru.cloud www.194-67-99-161.regru.cloud 194.67.99.161;
    ssl_certificate "/var/www/httpd-cert/www-root/194-67-99-161.regru.cloud.crt";
    ssl_certificate_key "/var/www/httpd-cert/www-root/194-67-99-161.regru.cloud.key";
    ssl_ciphers EECDH:+AES256:-3DES:RSA+AES:!NULL:!RC4;
    ssl_prefer_server_ciphers on;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;
    ssl_dhparam /etc/ssl/certs/dhparam4096.pem;
    charset off;
    index index.html;
    root {WEB_ROOT};
    disable_symlinks if_not_owner from=$root_path;
    set $root_path {WEB_ROOT};
    access_log /var/www/httpd-logs/194-67-99-161.regru.cloud.access.log;
    error_log /var/www/httpd-logs/194-67-99-161.regru.cloud.error.log notice;
    listen 192.168.0.186:443 ssl default_server;

    location /api/ {{
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}

    location /uploads/ {{
        alias {WEB_ROOT}/uploads/;
        access_log off;
        expires 7d;
    }}

    location /admin/ {{
        alias {WEB_ROOT}/admin/;
        index dashboard.html;
        try_files $uri $uri/ /admin/dashboard.html;
    }}

    location / {{
        try_files $uri $uri/ /index.html;
    }}
}}
"""

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=30)

    try:
        run(client, f"cat > {VHOST_PATH} << 'EOF'\n{nginx_conf}EOF")
        run(client, "nginx -t")
        run(client, "systemctl reload nginx")
        run(client, "curl -sS -I http://127.0.0.1/api/collections")
        run(client, "curl -sS -I http://127.0.0.1/")
    finally:
        client.close()

    print("\nDONE")


if __name__ == "__main__":
    main()
