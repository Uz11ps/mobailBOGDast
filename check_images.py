import paramiko
import sys

def check_images(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        print("--- Checking Collection Images ---")
        stdin, stdout, stderr = client.exec_command("sudo -u postgres psql -d charity_db -c 'SELECT title, \"imageUrl\", images FROM collection;'")
        print(stdout.read().decode())
        
        print("\n--- Checking Gallery Images ---")
        stdin, stdout, stderr = client.exec_command("sudo -u postgres psql -d charity_db -c 'SELECT title, \"imageUrl\" FROM gallery_item LIMIT 10;'")
        print(stdout.read().decode())

        print("\n--- Checking News Images ---")
        stdin, stdout, stderr = client.exec_command("sudo -u postgres psql -d charity_db -c 'SELECT title, \"imageUrl\" FROM news LIMIT 5;'")
        print(stdout.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

check_images(hostname, username, password)
