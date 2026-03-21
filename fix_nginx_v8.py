import paramiko
import sys

def fix_nginx_v8(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # 1. Check charity.conf again
        print("--- charity.conf ---")
        stdin, stdout, stderr = client.exec_command("cat /etc/nginx/conf.d/charity.conf")
        content = stdout.read().decode()
        print(content)
        
        # 2. Fix the location - move it inside the FIRST server block (the SSL one)
        if "location /uploads/" in content:
            import re
            # Remove it first
            content = re.sub(r'location /uploads/ \{.*?\n\s+\}', '', content, flags=re.DOTALL)
            
            # Find the first server { block and insert after it
            server_match = re.search(r'server \{', content)
            if server_match:
                insert_pos = server_match.end()
                new_location = """
    location /uploads/ {
        alias /var/www/charity_web/uploads/;
        autoindex on;
        allow all;
    }
"""
                content = content[:insert_pos] + new_location + content[insert_pos:]
                
                with open("charity_fixed_v2.conf", "w") as f:
                    f.write(content)
                
                sftp = client.open_sftp()
                sftp.put("charity_fixed_v2.conf", "/tmp/charity_fixed_v2.conf")
                sftp.close()
                
                client.exec_command("sudo mv /tmp/charity_fixed_v2.conf /etc/nginx/conf.d/charity.conf")
                client.exec_command("sudo nginx -t && sudo systemctl reload nginx")
                print("Nginx reloaded.")
        
        # 3. Verify via HTTPS locally (ignore cert)
        print("\n--- Final Verification ---")
        stdin, stdout, stderr = client.exec_command("curl -kI https://localhost/uploads/image0.jpeg")
        print(f"HTTP check: {stdout.read().decode()}")

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

fix_nginx_v8(hostname, username, password)
