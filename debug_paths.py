import paramiko
import sys

def debug_paths(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        cmds = [
            "pwd",
            "ls -l ~/mobailBOGDast/user_panel/index.html",
            "ls -l /var/www/charity_web/index.html",
            "cat /etc/nginx/nginx.conf | grep include",
            "ls -la /etc/nginx/conf.d/",
            "find /etc/nginx -name '*.conf' -exec grep -l 'xn--80adnee0afc6kza.com' {} +"
        ]
        
        for cmd in cmds:
            print(f"\n--- {cmd} ---")
            stdin, stdout, stderr = client.exec_command(cmd)
            print(stdout.read().decode())
            print(stderr.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

debug_paths(hostname, username, password)
