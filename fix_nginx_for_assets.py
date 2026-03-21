# -*- coding: utf-8 -*-
import paramiko
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def fix_nginx_config(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Читаем текущую конфигурацию nginx
        print("Чтение текущей конфигурации nginx...")
        stdin, stdout, stderr = client.exec_command("cat /etc/nginx/sites-available/charity_web")
        current_config = stdout.read().decode()
        print("Текущая конфигурация:")
        print(current_config)
        
        # Проверяем, есть ли уже location для assets
        if 'location /user_panel/assets' not in current_config:
            print("\nДобавление location для assets в nginx конфигурацию...")
            
            # Создаем новую конфигурацию с поддержкой assets
            new_config = current_config
            
            # Добавляем location для assets перед закрывающей скобкой server
            if 'location /uploads/' in new_config:
                # Вставляем после location /uploads/
                insert_pos = new_config.find('location /uploads/')
                end_pos = new_config.find('\n    }', insert_pos)
                if end_pos != -1:
                    assets_location = '''
    location /user_panel/assets/ {
        alias /var/www/charity_web/user_panel/assets/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
'''
                    new_config = new_config[:end_pos + len('\n    }')] + assets_location + new_config[end_pos + len('\n    }'):]
            else:
                # Добавляем перед закрывающей скобкой server
                insert_pos = new_config.rfind('}')
                assets_location = '''
    location /user_panel/assets/ {
        alias /var/www/charity_web/user_panel/assets/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
'''
                new_config = new_config[:insert_pos] + assets_location + new_config[insert_pos:]
            
            # Сохраняем новую конфигурацию
            sftp = client.open_sftp()
            with sftp.open('/tmp/nginx_new_config', 'w') as f:
                f.write(new_config)
            sftp.close()
            
            # Копируем новую конфигурацию
            client.exec_command("sudo cp /tmp/nginx_new_config /etc/nginx/sites-available/charity_web")
            
            # Проверяем конфигурацию
            print("Проверка конфигурации nginx...")
            stdin, stdout, stderr = client.exec_command("sudo nginx -t")
            result = stdout.read().decode()
            error = stderr.read().decode()
            print(result)
            if error:
                print("Ошибки:", error)
            
            if "successful" in result or "successful" in error.lower():
                print("Перезагрузка nginx...")
                client.exec_command("sudo systemctl reload nginx")
                print("[OK] Nginx перезагружен")
            else:
                print("[ERROR] Ошибка в конфигурации nginx, откатываем изменения")
                client.exec_command("sudo cp /etc/nginx/sites-available/charity_web.bak /etc/nginx/sites-available/charity_web 2>/dev/null || echo 'Backup not found'")
        else:
            print("[INFO] Конфигурация для assets уже существует")
            # Просто перезагружаем nginx
            client.exec_command("sudo systemctl reload nginx")
        
        # Проверяем доступность файла
        print("\n--- Проверка доступности логотипа ---")
        stdin, stdout, stderr = client.exec_command("curl -I http://localhost/user_panel/assets/logo.png 2>&1 | head -10")
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
    
    fix_nginx_config(hostname, username, password)
