import paramiko
import sys

def debug_nginx_config(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        print("--- Nginx Config File Content ---")
        stdin, stdout, stderr = client.exec_command("cat /etc/nginx/sites-available/charity_web")
        print(stdout.read().decode())
        
        print("\n--- Checking Uploads Directory ---")
        stdin, stdout, stderr = client.exec_command("ls -la /var/www/charity_web/uploads/")
        print(stdout.read().decode())
        
        print("\n--- Testing local file access via curl ---")
        stdin, stdout, stderr = client.exec_command("curl -I http://localhost/uploads/image0.jpeg")
        print(stdout.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

debug_nginx_config(hostname, username, password)
