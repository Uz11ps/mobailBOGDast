import paramiko
import sys

def fix_nginx_v7(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # 1. Check charity.conf
        print("--- charity.conf ---")
        stdin, stdout, stderr = client.exec_command("cat /etc/nginx/conf.d/charity.conf")
        content = stdout.read().decode()
        print(content)
        
        # 2. Add /uploads/ to charity.conf
        if "location /uploads/" not in content:
            print("Adding /uploads/ to charity.conf...")
            new_location = """
    location /uploads/ {
        alias /var/www/charity_web/uploads/;
        autoindex on;
        allow all;
    }
"""
            # Insert before the last closing brace
            last_brace_idx = content.rfind('}')
            new_content = content[:last_brace_idx] + new_location + content[last_brace_idx:]
            
            with open("charity_fixed.conf", "w") as f:
                f.write(new_content)
            
            sftp = client.open_sftp()
            sftp.put("charity_fixed.conf", "/tmp/charity_fixed.conf")
            sftp.close()
            
            client.exec_command("sudo mv /tmp/charity_fixed.conf /etc/nginx/conf.d/charity.conf")
            client.exec_command("sudo nginx -t && sudo systemctl reload nginx")
            print("Nginx reloaded.")
        
        # 3. Verify
        print("\n--- Final Verification ---")
        stdin, stdout, stderr = client.exec_command("curl -I http://localhost/uploads/image0.jpeg")
        print(f"HTTP check: {stdout.read().decode()}")

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

fix_nginx_v7(hostname, username, password)
