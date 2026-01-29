import paramiko
import sys

def check_server(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        print("--- Nginx Config ---")
        stdin, stdout, stderr = client.exec_command("ls /etc/nginx/sites-enabled/")
        configs = stdout.read().decode().split()
        for cfg in configs:
            print(f"\nConfig: {cfg}")
            stdin, stdout, stderr = client.exec_command(f"cat /etc/nginx/sites-enabled/{cfg}")
            print(stdout.read().decode())
        
        print("\n--- Directory Content /var/www/charity_web ---")
        stdin, stdout, stderr = client.exec_command("ls -la /var/www/charity_web")
        print(stdout.read().decode())
        
        print("\n--- Git Status in repo ---")
        stdin, stdout, stderr = client.exec_command("cd ~/mobailBOGDast && git log -1")
        print(stdout.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

check_server(hostname, username, password)
