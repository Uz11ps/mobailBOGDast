import paramiko
import sys

def final_fix_all(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # 1. Copy images from /root/mobailBOGDast/img to /var/www/charity_web/uploads
        print("--- Copying images to web directory ---")
        client.exec_command("sudo mkdir -p /var/www/charity_web/uploads")
        client.exec_command("sudo cp /root/mobailBOGDast/img/*.jpeg /var/www/charity_web/uploads/")
        client.exec_command("sudo chmod -R 755 /var/www/charity_web/uploads")
        
        # 2. Fix Nginx Config
        nginx_conf_path = "/etc/nginx/sites-available/charity_web"
        # Create a clean, simple config that definitely works
        simple_config = """
server {
    listen 80;
    server_name xn--80adnee0afc6kza.com;

    location / {
        root /var/www/charity_web;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:3000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /uploads/ {
        alias /var/www/charity_web/uploads/;
        autoindex on;
        allow all;
    }

    location /admin {
        alias /var/www/charity_web/admin;
        index dashboard.html;
        try_files $uri $uri/ /admin/dashboard.html;
    }
}
"""
        with open("nginx_final", "w") as f:
            f.write(simple_config)
            
        sftp = client.open_sftp()
        sftp.put("nginx_final", "/tmp/nginx_final")
        sftp.close()
        
        client.exec_command(f"sudo mv /tmp/nginx_final {nginx_conf_path}")
        client.exec_command("sudo nginx -t && sudo systemctl reload nginx")
        
        # 3. Verify
        print("\n--- Final Verification ---")
        stdin, stdout, stderr = client.exec_command("ls -la /var/www/charity_web/uploads/image0.jpeg")
        print(f"File check: {stdout.read().decode()}")
        
        stdin, stdout, stderr = client.exec_command("curl -I http://localhost/uploads/image0.jpeg")
        print(f"HTTP check: {stdout.read().decode()}")

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

final_fix_all(hostname, username, password)
