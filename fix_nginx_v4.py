import paramiko
import sys

def fix_nginx_v4(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # 1. List sites-available
        print("--- Nginx available sites ---")
        stdin, stdout, stderr = client.exec_command("ls /etc/nginx/sites-available/")
        print(stdout.read().decode())
        
        # 2. Check where Nginx is actually looking
        print("--- Nginx process info ---")
        stdin, stdout, stderr = client.exec_command("ps aux | grep nginx")
        print(stdout.read().decode())
        
        # 3. Check /etc/nginx/nginx.conf
        print("--- nginx.conf ---")
        stdin, stdout, stderr = client.exec_command("cat /etc/nginx/nginx.conf")
        print(stdout.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

fix_nginx_v4(hostname, username, password)
