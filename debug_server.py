import paramiko
import sys

def debug_server_path(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        print("--- Checking current directory and branch ---")
        stdin, stdout, stderr = client.exec_command("cd ~/mobailBOGDast && pwd && git branch && git log -1 --oneline")
        print(stdout.read().decode())
        
        print("\n--- Checking backend/src/index.ts content ---")
        stdin, stdout, stderr = client.exec_command("cat ~/mobailBOGDast/backend/src/index.ts")
        print(stdout.read().decode())
        
        print("\n--- Checking PM2 process list ---")
        stdin, stdout, stderr = client.exec_command("pm2 list")
        print(stdout.read().decode())
        
        print("\n--- Checking PM2 process info for charity-api ---")
        stdin, stdout, stderr = client.exec_command("pm2 show charity-api")
        print(stdout.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

debug_server_path(hostname, username, password)
