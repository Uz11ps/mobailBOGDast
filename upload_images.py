import paramiko
import os

def upload_images(hostname, username, password, local_dir, remote_dir):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Create remote directory if not exists
        client.exec_command(f"mkdir -p {remote_dir}")
        
        sftp = client.open_sftp()
        
        files = [f for f in os.listdir(local_dir) if f.endswith(('.jpeg', '.jpg', '.png', '.webp'))]
        print(f"Uploading {len(files)} images...")
        
        for f in files:
            local_path = os.path.join(local_dir, f)
            remote_path = os.path.join(remote_dir, f)
            sftp.put(local_path, remote_path)
            # print(f"Uploaded {f}")
            
        sftp.close()
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

upload_images(hostname, username, password, local_img_dir, remote_img_dir)
