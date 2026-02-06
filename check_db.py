import paramiko
import sys

def check_db_content(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        print("--- Checking Story table content ---")
        stdin, stdout, stderr = client.exec_command("sudo -u postgres psql -d charity_db -c 'SELECT * FROM story;'")
        print(stdout.read().decode())
        
        print("\n--- Checking API logs ---")
        stdin, stdout, stderr = client.exec_command("pm2 logs charity-api --lines 20 --no-colors")
        print(stdout.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

check_db_content(hostname, username, password)
