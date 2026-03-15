# -*- coding: utf-8 -*-
import paramiko
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def check_and_fix(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Проверяем есть ли SSL конфигурация
        print("--- Проверка SSL конфигурации ---")
        stdin, stdout, stderr = client.exec_command("ls -la /etc/nginx/sites-available/ | grep -i ssl")
        ssl_configs = stdout.read().decode()
        print(ssl_configs)
        
        # Проверяем доступность через HTTPS
        print("\n--- Проверка через HTTPS ---")
        stdin, stdout, stderr = client.exec_command("curl -k -I https://localhost/user_panel/assets/logo.png 2>&1 | head -5")
        print(stdout.read().decode())
        
        # Простое решение - копируем логотип также в корневую папку для прямого доступа
        print("\n--- Копирование логотипа в корневую папку для прямого доступа ---")
        client.exec_command("sudo mkdir -p /var/www/charity_web/assets")
        client.exec_command("sudo cp /var/www/charity_web/user_panel/assets/logo.png /var/www/charity_web/assets/logo.png")
        client.exec_command("sudo chmod 644 /var/www/charity_web/assets/logo.png")
        client.exec_command("sudo chown www-data:www-data /var/www/charity_web/assets/logo.png")
        
        # Обновляем index.html чтобы использовать прямой путь
        print("\n--- Обновление путей в index.html ---")
        stdin, stdout, stderr = client.exec_command("sed -i 's|\\./assets/logo\\.png|/assets/logo.png|g' /var/www/charity_web/user_panel/index.html")
        stdout.channel.recv_exit_status()
        
        # Проверяем что изменения применены
        print("\n--- Проверка изменений в index.html ---")
        stdin, stdout, stderr = client.exec_command("grep -n 'logo.png' /var/www/charity_web/user_panel/index.html | head -5")
        print(stdout.read().decode())
        
        # Проверяем доступность через прямой путь
        print("\n--- Проверка доступности через /assets/logo.png ---")
        stdin, stdout, stderr = client.exec_command("curl -I http://localhost/assets/logo.png 2>&1 | head -5")
        print(stdout.read().decode())
        
        client.close()
        print("\n[SUCCESS] Логотип скопирован в корневую папку!")
        print("[INFO] Теперь логотип доступен по пути /assets/logo.png")
        print("[INFO] Проверьте сайт: https://xn--80adnee0afc6kza.com/")
        
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    hostname = 'xn--80adnee0afc6kza.com'
    username = 'root'
    password = 'kxNG6YOk32s0qWNo'
    
    check_and_fix(hostname, username, password)
