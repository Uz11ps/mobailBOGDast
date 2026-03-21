# -*- coding: utf-8 -*-
import paramiko
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def check_current_state(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Проверяем текущий index.html
        print("\n--- Проверка текущего index.html (первые 50 строк) ---")
        stdin, stdout, stderr = client.exec_command("head -50 /var/www/charity_web/user_panel/index.html")
        print(stdout.read().decode())
        
        # Проверяем наличие логотипа в navbar
        print("\n--- Проверка логотипа в navbar ---")
        stdin, stdout, stderr = client.exec_command("grep -A 2 -B 2 'navbar-brand' /var/www/charity_web/user_panel/index.html | head -10")
        print(stdout.read().decode())
        
        # Проверяем ссылку на влияние
        print("\n--- Проверка ссылки #влияние ---")
        stdin, stdout, stderr = client.exec_command("grep -n 'влияние' /var/www/charity_web/user_panel/index.html")
        print(stdout.read().decode())
        
        # Проверяем наличие логотипа на сервере
        print("\n--- Проверка файла логотипа ---")
        stdin, stdout, stderr = client.exec_command("ls -la /var/www/charity_web/assets/logo.png")
        print(stdout.read().decode())
        
        # Проверяем доступность через веб
        print("\n--- Проверка доступности логотипа через HTTPS ---")
        stdin, stdout, stderr = client.exec_command("curl -k -I https://localhost/assets/logo.png 2>&1 | head -5")
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
    
    check_current_state(hostname, username, password)
