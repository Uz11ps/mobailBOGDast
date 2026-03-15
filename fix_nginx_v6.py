import paramiko
import sys

def fix_nginx_v6(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # 1. List /etc/nginx/conf.d/
        print("--- Nginx conf.d ---")
        stdin, stdout, stderr = client.exec_command("ls /etc/nginx/conf.d/")
        print(stdout.read().decode())
        
        # 2. Check if charity_web is enabled
        print("--- Enabling charity_web ---")
        client.exec_command("sudo ln -s /etc/nginx/sites-available/charity_web /etc/nginx/sites-enabled/")
        client.exec_command("sudo nginx -t && sudo systemctl reload nginx")
        
        # 3. Verify
        print("\n--- Final Verification ---")
        stdin, stdout, stderr = client.exec_command("curl -I http://localhost/uploads/image0.jpeg")
        print(f"HTTP check: {stdout.read().decode()}")

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

fix_nginx_v6(hostname, username, password)
