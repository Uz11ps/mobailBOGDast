import paramiko
import sys

def configure_nginx_uploads(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Add location block for /uploads/ to nginx config
        nginx_conf_path = "/etc/nginx/sites-available/charity_web"
        
        # Read current config
        stdin, stdout, stderr = client.exec_command(f"cat {nginx_conf_path}")
        config = stdout.read().decode()
        
        if "location /uploads/" not in config:
            print("Adding /uploads/ location to Nginx config...")
            # Insert before the last closing brace
            new_location = """
    location /uploads/ {
        alias /var/www/charity_web/uploads/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
"""
            # Find the last '}'
            last_brace_idx = config.rfind('}')
            new_config = config[:last_brace_idx] + new_location + config[last_brace_idx:]
            
            # Write back to a temp file then sudo mv
            with open("nginx_temp", "w") as f:
                f.write(new_config)
            
            sftp = client.open_sftp()
            sftp.put("nginx_temp", "/tmp/nginx_temp")
            sftp.close()
            
            client.exec_command(f"sudo mv /tmp/nginx_temp {nginx_conf_path}")
            client.exec_command("sudo nginx -t && sudo systemctl reload nginx")
            print("Nginx reloaded.")
        else:
            print("/uploads/ already exists in Nginx config.")

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

configure_nginx_uploads(hostname, username, password)
