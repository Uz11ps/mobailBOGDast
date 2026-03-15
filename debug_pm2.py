import paramiko
import sys

def debug_pm2(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        print("--- PM2 Show charity-api ---")
        stdin, stdout, stderr = client.exec_command("pm2 show charity-api")
        output = stdout.read().decode('utf-8', 'ignore')
        print(output)
        
        print("\n--- Testing localhost:3000/api/stories ---")
        stdin, stdout, stderr = client.exec_command("curl -v http://localhost:3000/api/stories")
        print(stdout.read().decode('utf-8', 'ignore'))
        print(stderr.read().decode('utf-8', 'ignore'))

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

debug_pm2(hostname, username, password)
