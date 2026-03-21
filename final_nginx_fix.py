# -*- coding: utf-8 -*-
import paramiko
import sys
import time

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def final_fix(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Используем более простой подход - просто добавляем в location / 
        # или используем более специфичный location с точным совпадением
        nginx_config = """server {
    listen 80;
    server_name xn--80adnee0afc6kza.com;

    # Статические файлы assets - должно быть ПЕРЕД location /
    location ~ ^/user_panel/assets/(.*)$ {
        alias /var/www/charity_web/user_panel/assets/$1;
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
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
        with sftp.open('/tmp/nginx_final_fix', 'w') as f:
            f.write(nginx_config)
        sftp.close()
        
        # Устанавливаем
        print("Установка финальной конфигурации...")
        client.exec_command("sudo cp /tmp/nginx_final_fix /etc/nginx/sites-available/charity_web")
        
        # Проверяем
        stdin, stdout, stderr = client.exec_command("sudo nginx -t")
        result = stdout.read().decode()
        error = stderr.read().decode()
        print("Результат проверки:")
        print(result)
        if error:
            print("Ошибки:", error)
        
        if "successful" in result or "successful" in error.lower():
            print("Перезагрузка nginx...")
            stdin, stdout, stderr = client.exec_command("sudo systemctl reload nginx")
            time.sleep(2)  # Даем время на перезагрузку
            
            # Проверяем доступность
            print("\n--- Проверка доступности логотипа ---")
            stdin, stdout, stderr = client.exec_command("curl -I http://localhost/user_panel/assets/logo.png 2>&1 | head -8")
            result = stdout.read().decode()
            print(result)
            
            if "200 OK" in result or "HTTP/1.1 200" in result:
                print("\n[SUCCESS] Логотип теперь доступен!")
            else:
                print("\n[INFO] Проверяем альтернативный путь...")
                # Попробуем через прямой путь
                stdin, stdout, stderr = client.exec_command("curl -I http://xn--80adnee0afc6kza.com/user_panel/assets/logo.png 2>&1 | head -5")
                print(stdout.read().decode())
        else:
            print("[ERROR] Ошибка в конфигурации")
        
        client.close()
        print("\n[INFO] Проверьте сайт: https://xn--80adnee0afc6kza.com/")
        print("[TIP] Очистите кэш браузера (Ctrl+F5) если изменения не видны")
        
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    hostname = 'xn--80adnee0afc6kza.com'
    username = 'root'
    password = 'kxNG6YOk32s0qWNo'
    
    final_fix(hostname, username, password)
