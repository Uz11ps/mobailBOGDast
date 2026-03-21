import paramiko
import sys

def add_stories(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Check table names
        stdin, stdout, stderr = client.exec_command("sudo -u postgres psql -d charity_db -c '\\dt'")
        print("--- Tables in DB ---")
        print(stdout.read().decode())

        client.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

add_stories(hostname, username, password)
