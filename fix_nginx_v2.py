import paramiko
import sys

def fix_nginx_and_verify(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # 1. Check where the files actually are
        print("--- Finding image0.jpeg ---")
        stdin, stdout, stderr = client.exec_command("find /var/www -name image0.jpeg")
        found_paths = stdout.read().decode().splitlines()
        print(f"Found at: {found_paths}")
        
        if not found_paths:
            print("CRITICAL: image0.jpeg not found anywhere in /var/www")
            # Let's check /root/mobailBOGDast just in case
            stdin, stdout, stderr = client.exec_command("find /root -name image0.jpeg")
            print(f"Found in root: {stdout.read().decode()}")
        
        # 2. Fix Nginx config - ensure it's inside the server block
        nginx_conf_path = "/etc/nginx/sites-available/charity_web"
        stdin, stdout, stderr = client.exec_command(f"cat {nginx_conf_path}")
        config = stdout.read().decode()
        
        print("--- Current Nginx Config ---")
        print(config)
        
        # If it's outside the server block, we need to move it inside
        if "location /uploads/" in config:
            # Simple way: remove it and re-add it inside the server block
            import re
            config = re.sub(r'location /uploads/ \{.*?\n\s+\}', '', config, flags=re.DOTALL)
            
            # Find the first server { block and insert after it
            server_match = re.search(r'server \{', config)
            if server_match:
                insert_pos = server_match.end()
                new_location = """
    location /uploads/ {
        alias /var/www/charity_web/uploads/;
        autoindex on;
        allow all;
    }
"""
                config = config[:insert_pos] + new_location + config[insert_pos:]
                
                with open("nginx_fixed", "w") as f:
                    f.write(config)
                
                sftp = client.open_sftp()
                sftp.put("nginx_fixed", "/tmp/nginx_fixed")
                sftp.close()
                
                client.exec_command(f"sudo mv /tmp/nginx_fixed {nginx_conf_path}")
                client.exec_command("sudo nginx -t && sudo systemctl reload nginx")
                print("Nginx fixed and reloaded.")
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

fix_nginx_and_verify(hostname, username, password)
