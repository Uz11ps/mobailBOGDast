# -*- coding: utf-8 -*-
import paramiko
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def check_ssl_config(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Проверяем все конфигурации nginx
        print("\n=== ВСЕ КОНФИГУРАЦИИ NGINX ===")
        stdin, stdout, stderr = client.exec_command("ls -la /etc/nginx/sites-available/")
        print(stdout.read().decode())
        
        stdin, stdout, stderr = client.exec_command("ls -la /etc/nginx/sites-enabled/")
        print("\n=== АКТИВНЫЕ КОНФИГУРАЦИИ ===")
        print(stdout.read().decode())
        
        # Проверяем есть ли SSL конфигурация
        print("\n=== ПРОВЕРКА SSL КОНФИГУРАЦИИ ===")
        stdin, stdout, stderr = client.exec_command("grep -r 'server_name.*xn--80adnee0afc6kza.com' /etc/nginx/sites-available/")
        ssl_configs = stdout.read().decode()
        print(ssl_configs if ssl_configs else "Не найдено")
        
        # Проверяем через HTTPS
        print("\n=== ПРОВЕРКА ЧЕРЕЗ HTTPS ===")
        stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/ | head -15")
        https_response = stdout.read().decode()
        print(https_response)
        
        # Проверяем логотип в HTTPS ответе
        print("\n=== ПРОВЕРКА ЛОГОТИПА В HTTPS ОТВЕТЕ ===")
        stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/ | grep -i 'logo.png' | head -3")
        logo_https = stdout.read().decode()
        print(logo_https if logo_https else "НЕ НАЙДЕНО!")
        
        # Проверяем размер файла index.html
        print("\n=== РАЗМЕР ФАЙЛА INDEX.HTML ===")
        stdin, stdout, stderr = client.exec_command("ls -lh /var/www/charity_web/index.html")
        print(stdout.read().decode())
        
        # Проверяем дату изменения
        stdin, stdout, stderr = client.exec_command("stat /var/www/charity_web/index.html | grep Modify")
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
    
    check_ssl_config(hostname, username, password)
