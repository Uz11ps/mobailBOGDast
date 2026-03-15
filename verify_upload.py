# -*- coding: utf-8 -*-
import paramiko
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def verify_upload(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу для проверки...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Проверяем структуру файлов
        print("\n--- Проверка структуры файлов ---")
        stdin, stdout, stderr = client.exec_command("ls -la /var/www/charity_web/user_panel/")
        print(stdout.read().decode())
        
        stdin, stdout, stderr = client.exec_command("ls -la /var/www/charity_web/user_panel/assets/")
        print(stdout.read().decode())
        
        # Проверяем содержимое index.html (первые строки)
        print("\n--- Проверка favicon в index.html ---")
        stdin, stdout, stderr = client.exec_command("grep -n 'favicon\\|logo.png' /var/www/charity_web/user_panel/index.html | head -5")
        print(stdout.read().decode())
        
        # Проверяем ссылку на влияние
        print("\n--- Проверка ссылки #влияние ---")
        stdin, stdout, stderr = client.exec_command("grep -n 'влияние' /var/www/charity_web/user_panel/index.html | head -3")
        print(stdout.read().decode())
        
        # Проверяем доступность файла через веб-сервер
        print("\n--- Проверка доступности логотипа через HTTP ---")
        stdin, stdout, stderr = client.exec_command("curl -I http://localhost/user_panel/assets/logo.png 2>&1 | head -5")
        print(stdout.read().decode())
        
        client.close()
        print("\n[SUCCESS] Проверка завершена!")
        
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    hostname = 'xn--80adnee0afc6kza.com'
    username = 'root'
    password = 'kxNG6YOk32s0qWNo'
    
    verify_upload(hostname, username, password)
