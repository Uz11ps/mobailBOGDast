import paramiko
import sys

def check_partners_and_stories(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        print("--- Checking Partners ---")
        stdin, stdout, stderr = client.exec_command("sudo -u postgres psql -d charity_db -c 'SELECT * FROM partner;'")
        print(stdout.read().decode())
        
        print("\n--- Checking Stories ---")
        stdin, stdout, stderr = client.exec_command("sudo -u postgres psql -d charity_db -c 'SELECT * FROM story;'")
        print(stdout.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

check_partners_and_stories(hostname, username, password)
