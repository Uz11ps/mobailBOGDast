import paramiko
import sys

def fix_nginx_v5(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # 1. Check /etc/nginx/vhosts/
        print("--- Nginx vhosts ---")
        stdin, stdout, stderr = client.exec_command("ls -R /etc/nginx/vhosts/")
        print(stdout.read().decode())
        
        # 2. Check /etc/nginx/vhosts-includes/
        print("--- Nginx vhosts-includes ---")
        stdin, stdout, stderr = client.exec_command("ls /etc/nginx/vhosts-includes/")
        print(stdout.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

fix_nginx_v5(hostname, username, password)
