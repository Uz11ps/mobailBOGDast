import paramiko
import os

def upload_images_v2(hostname, username, password, local_dir, remote_dir):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Ensure directory exists and has correct permissions
        client.exec_command(f"sudo mkdir -p {remote_dir}")
        client.exec_command(f"sudo chown -R root:root {remote_dir}")
        client.exec_command(f"sudo chmod -R 755 {remote_dir}")
        
        sftp = client.open_sftp()
        
        files = [f for f in os.listdir(local_dir) if f.endswith(('.jpeg', '.jpg', '.png', '.webp'))]
        print(f"Uploading {len(files)} images to {remote_dir}...")
        
        for f in files:
            local_path = os.path.join(local_dir, f)
            remote_path = os.path.join(remote_dir, f)
            # Use a temporary path first if direct upload fails due to permissions
            temp_path = f"/tmp/{f}"
            sftp.put(local_path, temp_path)
            client.exec_command(f"sudo mv {temp_path} {remote_path}")
            client.exec_command(f"sudo chmod 644 {remote_path}")
            
        sftp.close()
        
        # Double check
        stdin, stdout, stderr = client.exec_command(f"ls -la {remote_dir} | head -n 10")
        print("Remote directory content check:")
        print(stdout.read().decode())
        
        client.close()
        print("Upload complete.")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'
local_img_dir = 'img'
remote_img_dir = '/var/www/charity_web/uploads'

upload_images_v2(hostname, username, password, local_img_dir, remote_img_dir)
