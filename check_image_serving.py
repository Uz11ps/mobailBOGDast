import paramiko
import sys

def check_image_serving(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        print("--- Testing image access via curl ---")
        # Check if the image is accessible and what the content type is
        stdin, stdout, stderr = client.exec_command("curl -I https://xn--80adnee0afc6kza.com/uploads/image0.jpeg")
        print(stdout.read().decode())
        
        print("\n--- Checking file existence and size ---")
        stdin, stdout, stderr = client.exec_command("ls -lh /var/www/charity_web/uploads/image0.jpeg")
        print(stdout.read().decode())
        
        print("\n--- Checking Nginx error logs ---")
        stdin, stdout, stderr = client.exec_command("sudo tail -n 20 /var/log/nginx/error.log")
        print(stdout.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

check_image_serving(hostname, username, password)
