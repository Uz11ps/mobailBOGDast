import paramiko

HOST = "194.67.99.161"
USER = "root"
PASSWORD = "BfiR0QRRjX7NDI7A"


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
    print(f"exit_code={code}")


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=30)
    try:
        run(client, "sed -n '1,240p' /etc/nginx/nginx.conf")
        run(client, "ls -la /etc/nginx")
        run(client, "ls -la /etc/nginx/sites-enabled")
        run(client, "ls -la /etc/nginx/sites-available")
        run(client, "ls -la /etc/nginx/vhosts")
        run(client, "ls -la /etc/nginx/vhosts/* || true")
        run(client, "sed -n '1,240p' /etc/nginx/vhosts/*/*.conf || true")
        run(client, "ls -la /usr/local/mgr5/etc || true")
        run(client, "ls -la /etc/apache2/sites-enabled || true")
        run(client, "apache2 -v || true")
        run(client, "systemctl status nginx --no-pager -l | sed -n '1,80p'")
        run(client, "ss -ltnp | sed -n '1,120p'")
    finally:
        client.close()


if __name__ == "__main__":
    main()
