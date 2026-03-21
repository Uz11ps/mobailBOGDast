# -*- coding: utf-8 -*-
import paramiko
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def fix_nginx_properly(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Создаем правильную конфигурацию с location для assets ПЕРЕД location /
        nginx_config = """server {
    listen 80;
    server_name xn--80adnee0afc6kza.com;

    location /user_panel/assets/ {
        alias /var/www/charity_web/user_panel/assets/;
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
        with sftp.open('/tmp/nginx_config_fixed', 'w') as f:
            f.write(nginx_config)
        sftp.close()
        
        # Делаем backup текущей конфигурации
        print("Создание backup текущей конфигурации...")
        client.exec_command("sudo cp /etc/nginx/sites-available/charity_web /etc/nginx/sites-available/charity_web.backup.$(date +%Y%m%d_%H%M%S)")
        
        # Копируем новую конфигурацию
        print("Установка новой конфигурации...")
        client.exec_command("sudo cp /tmp/nginx_config_fixed /etc/nginx/sites-available/charity_web")
        
        # Проверяем конфигурацию
        print("Проверка конфигурации nginx...")
        stdin, stdout, stderr = client.exec_command("sudo nginx -t")
        result = stdout.read().decode()
        error = stderr.read().decode()
        print(result)
        if error and "successful" not in error.lower():
            print("Ошибки:", error)
        
        if "successful" in result or "successful" in error.lower():
            print("Перезагрузка nginx...")
            stdin, stdout, stderr = client.exec_command("sudo systemctl reload nginx")
            stdout.channel.recv_exit_status()
            print("[OK] Nginx перезагружен")
        else:
            print("[ERROR] Ошибка в конфигурации nginx")
            return
        
        # Проверяем доступность файла
        print("\n--- Проверка доступности логотипа ---")
        stdin, stdout, stderr = client.exec_command("curl -I http://localhost/user_panel/assets/logo.png 2>&1 | head -10")
        result = stdout.read().decode()
        print(result)
        
        if "200 OK" in result or "HTTP/1.1 200" in result:
            print("[SUCCESS] Логотип доступен!")
        else:
            print("[WARNING] Логотип все еще недоступен, проверяем путь...")
            stdin, stdout, stderr = client.exec_command("ls -la /var/www/charity_web/user_panel/assets/logo.png")
            print(stdout.read().decode())
        
        client.close()
        print("\n[SUCCESS] Конфигурация обновлена!")
        
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    hostname = 'xn--80adnee0afc6kza.com'
    username = 'root'
    password = 'kxNG6YOk32s0qWNo'
    
    fix_nginx_properly(hostname, username, password)
