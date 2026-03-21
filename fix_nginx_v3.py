import paramiko
import sys

def fix_nginx_v3(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # 1. Check ALL nginx configs
        print("--- Nginx enabled sites ---")
        stdin, stdout, stderr = client.exec_command("ls /etc/nginx/sites-enabled/")
        print(stdout.read().decode())
        
        # 2. Check the default config
        print("--- Default config ---")
        stdin, stdout, stderr = client.exec_command("cat /etc/nginx/sites-enabled/default")
        print(stdout.read().decode())
        
        # 3. Check our config
        print("--- Our config ---")
        stdin, stdout, stderr = client.exec_command("cat /etc/nginx/sites-enabled/charity_web")
        print(stdout.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

fix_nginx_v3(hostname, username, password)
