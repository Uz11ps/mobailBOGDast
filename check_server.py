import paramiko
import sys

def check_server_files(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        print("--- Checking backend/src/index.ts on server ---")
        stdin, stdout, stderr = client.exec_command("cat /var/www/charity_web/backend/src/index.ts")
        print(stdout.read().decode())
        
        print("\n--- Checking backend/dist/index.js on server ---")
        stdin, stdout, stderr = client.exec_command("cat /var/www/charity_web/backend/dist/index.js")
        # Just check if stories is mentioned
        content = stdout.read().decode()
        if "/api/stories" in content:
            print("Found /api/stories in dist/index.js")
        else:
            print("NOT FOUND /api/stories in dist/index.js")

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

check_server_files(hostname, username, password)
