import paramiko
import sys

def force_update_all(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        school_images = "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&q=80&w=800"
        
        print("--- Forcing update on all collections ---")
        sql = f"UPDATE collection SET images = '{school_images}', category = 'Школы' WHERE images IS NULL OR images = '' OR category IS NULL OR category = '';"
        stdin, stdout, stderr = client.exec_command(f"sudo -u postgres psql -d charity_db -c \"{sql}\"")
        print(stdout.read().decode())
        
        print("--- Checking all collections now ---")
        stdin, stdout, stderr = client.exec_command("sudo -u postgres psql -d charity_db -c 'SELECT id, title, category, images FROM collection;'")
        print(stdout.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

force_update_all(hostname, username, password)
