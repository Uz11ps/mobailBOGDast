# -*- coding: utf-8 -*-
import paramiko
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def test_and_fix(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Проверяем текущую конфигурацию
        print("--- Текущая конфигурация nginx ---")
        stdin, stdout, stderr = client.exec_command("cat /etc/nginx/sites-available/charity_web")
        print(stdout.read().decode())
        
        # Тестируем прямой доступ к файлу
        print("\n--- Проверка прямого доступа к файлу ---")
        stdin, stdout, stderr = client.exec_command("file /var/www/charity_web/user_panel/assets/logo.png")
        print(stdout.read().decode())
        
        # Тестируем через root вместо alias
        print("\n--- Тестирование через root ---")
        stdin, stdout, stderr = client.exec_command("curl -I http://localhost/user_panel/assets/logo.png 2>&1")
        print(stdout.read().decode())
        
        # Создаем правильную конфигурацию с root вместо alias
        nginx_config = """server {
    listen 80;
    server_name xn--80adnee0afc6kza.com;

    location /user_panel/assets/ {
        root /var/www/charity_web;
        expires 30d;
        add_header Cache-Control "public, immutable";
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

    location / {
        root /var/www/charity_web;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
"""
        
        # Сохраняем конфигурацию
        sftp = client.open_sftp()
        with sftp.open('/tmp/nginx_config_root', 'w') as f:
            f.write(nginx_config)
        sftp.close()
        
        # Устанавливаем новую конфигурацию
        print("\nУстановка конфигурации с root...")
        client.exec_command("sudo cp /tmp/nginx_config_root /etc/nginx/sites-available/charity_web")
        
        # Проверяем и перезагружаем
        stdin, stdout, stderr = client.exec_command("sudo nginx -t")
        result = stdout.read().decode()
        print(result)
        
        if "successful" in result:
            client.exec_command("sudo systemctl reload nginx")
            print("[OK] Nginx перезагружен")
            
            # Проверяем доступность
            print("\n--- Финальная проверка ---")
            stdin, stdout, stderr = client.exec_command("curl -I http://localhost/user_panel/assets/logo.png 2>&1 | head -5")
            print(stdout.read().decode())
        
        client.close()
        
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    hostname = 'xn--80adnee0afc6kza.com'
    username = 'root'
    password = 'kxNG6YOk32s0qWNo'
    
    test_and_fix(hostname, username, password)
