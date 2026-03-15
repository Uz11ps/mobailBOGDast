# -*- coding: utf-8 -*-
import paramiko
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def deep_check(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # 1. Проверяем структуру директорий
        print("\n=== СТРУКТУРА ДИРЕКТОРИЙ ===")
        stdin, stdout, stderr = client.exec_command("ls -la /var/www/charity_web/")
        print(stdout.read().decode())
        
        # 2. Проверяем какой index.html используется
        print("\n=== ПРОВЕРКА INDEX.HTML ===")
        stdin, stdout, stderr = client.exec_command("find /var/www/charity_web -name 'index.html' -type f")
        index_files = stdout.read().decode()
        print("Найденные index.html файлы:")
        print(index_files)
        
        # 3. Проверяем конфигурацию nginx - какой root используется
        print("\n=== КОНФИГУРАЦИЯ NGINX ===")
        stdin, stdout, stderr = client.exec_command("cat /etc/nginx/sites-available/charity_web")
        nginx_config = stdout.read().decode()
        print(nginx_config)
        
        # 4. Проверяем какой файл реально отдается при запросе /
        print("\n=== ПРОВЕРКА РЕАЛЬНОГО ФАЙЛА ===")
        stdin, stdout, stderr = client.exec_command("curl -s http://localhost/ | head -20")
        actual_content = stdout.read().decode()
        print("Первые 20 строк реального ответа:")
        print(actual_content)
        
        # 5. Проверяем есть ли логотип в реальном ответе
        print("\n=== ПРОВЕРКА ЛОГОТИПА В РЕАЛЬНОМ ОТВЕТЕ ===")
        stdin, stdout, stderr = client.exec_command("curl -s http://localhost/ | grep -i 'logo.png' | head -5")
        logo_in_response = stdout.read().decode()
        print("Найденные упоминания logo.png:")
        print(logo_in_response if logo_in_response else "НЕ НАЙДЕНО!")
        
        # 6. Проверяем доступность логотипа
        print("\n=== ПРОВЕРКА ДОСТУПНОСТИ ЛОГОТИПА ===")
        stdin, stdout, stderr = client.exec_command("curl -I http://localhost/assets/logo.png 2>&1")
        logo_access = stdout.read().decode()
        print(logo_access)
        
        client.close()
        
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    hostname = 'xn--80adnee0afc6kza.com'
    username = 'root'
    password = 'kxNG6YOk32s0qWNo'
    
    deep_check(hostname, username, password)
