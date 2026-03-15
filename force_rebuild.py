import paramiko
import sys

def force_rebuild(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        commands = [
            "cd ~/mobailBOGDast/backend && rm -rf dist && npm run build",
            "pm2 restart charity-api",
            "pm2 save"
        ]
        
        for cmd in commands:
            print(f"Executing: {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd)
            print(stdout.read().decode('utf-8', 'ignore'))
            print(stderr.read().decode('utf-8', 'ignore'))

        client.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

force_rebuild(hostname, username, password)
