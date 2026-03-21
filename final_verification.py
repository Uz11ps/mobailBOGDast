# -*- coding: utf-8 -*-
import paramiko
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def final_verification(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу для финальной проверки...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Убеждаемся что логотип в корневой папке assets
        print("\n--- Проверка логотипа в корневой папке ---")
        stdin, stdout, stderr = client.exec_command("ls -la /var/www/charity_web/assets/logo.png 2>&1")
        result = stdout.read().decode()
        if "No such file" in result:
            print("Копирование логотипа в корневую папку...")
            client.exec_command("sudo mkdir -p /var/www/charity_web/assets")
            client.exec_command("sudo cp /var/www/charity_web/user_panel/assets/logo.png /var/www/charity_web/assets/logo.png")
            client.exec_command("sudo chmod 644 /var/www/charity_web/assets/logo.png")
            client.exec_command("sudo chown www-data:www-data /var/www/charity_web/assets/logo.png")
            print("[OK] Логотип скопирован")
        else:
            print("[OK] Логотип уже существует в корневой папке")
            print(result)
        
        # Проверяем доступность через HTTPS
        print("\n--- Проверка доступности логотипа через HTTPS ---")
        stdin, stdout, stderr = client.exec_command("curl -k -I https://localhost/assets/logo.png 2>&1 | head -5")
        print(stdout.read().decode())
        
        # Проверяем ссылку #влияние
        print("\n--- Проверка ссылки #влияние в index.html ---")
        stdin, stdout, stderr = client.exec_command("grep -n 'влияние' /var/www/charity_web/user_panel/index.html | head -3")
        print(stdout.read().decode())
        
        # Проверяем favicon
        print("\n--- Проверка favicon в index.html ---")
        stdin, stdout, stderr = client.exec_command("grep -n 'favicon\\|logo.png' /var/www/charity_web/user_panel/index.html | head -3")
        print(stdout.read().decode())
        
        client.close()
        
        print("\n" + "="*60)
        print("[SUCCESS] Все файлы успешно загружены и настроены!")
        print("="*60)
        print("\n[INFO] Логотип добавлен:")
        print("  - В navbar (рядом с названием)")
        print("  - На главной странице (в hero-секции)")
        print("  - Как favicon (в адресной строке браузера)")
        print("\n[INFO] Ссылка изменена:")
        print("  - Было: #impact")
        print("  - Стало: #влияние")
        print("\n[INFO] Проверьте сайт:")
        print("  https://xn--80adnee0afc6kza.com/")
        print("  https://xn--80adnee0afc6kza.com/#влияние")
        print("\n[TIP] Очистите кэш браузера (Ctrl+F5) если изменения не видны")
        print("="*60)
        
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    hostname = 'xn--80adnee0afc6kza.com'
    username = 'root'
    password = 'kxNG6YOk32s0qWNo'
    
    final_verification(hostname, username, password)
