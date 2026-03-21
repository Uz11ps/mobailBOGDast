import paramiko
import sys

def execute_commands(hostname, username, password, commands):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        for cmd in commands:
            stdin, stdout, stderr = client.exec_command(cmd)
            stdout.channel.recv_exit_status()
        client.close()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

commands = [
    "cd ~/mobailBOGDast && git clean -fd && git reset --hard && git pull",
    "cd ~/mobailBOGDast/backend && npm install && npm run build && pm2 restart charity-api",
    "cp ~/mobailBOGDast/user_panel/index.html /var/www/charity_web/index.html",
    "cp ~/mobailBOGDast/user_panel/profile.html /var/www/charity_web/profile.html",
    "cp ~/mobailBOGDast/admin_panel/dashboard.html /var/www/charity_web/admin/dashboard.html",
    "chown -R www-data:www-data /var/www/charity_web"
]

if execute_commands(hostname, username, password, commands):
    print("Server updated with premium UI!")
else:
    sys.exit(1)
