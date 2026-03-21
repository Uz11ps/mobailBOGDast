import paramiko
import sys

def check_api_response(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        print("--- Testing /api/stories endpoint ---")
        stdin, stdout, stderr = client.exec_command("curl -s http://localhost:3000/api/stories")
        print(stdout.read().decode())
        
        print("\n--- Checking for errors in PM2 logs ---")
        stdin, stdout, stderr = client.exec_command("pm2 logs charity-api --lines 50 --no-colors")
        print(stdout.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

check_api_response(hostname, username, password)
