# -*- coding: utf-8 -*-
import paramiko
import sys
import os

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def fix_root_index(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        sftp = client.open_sftp()
        
        # 1. Загружаем обновленный index.html напрямую в корень
        local_index = "user_panel/index.html"
        if os.path.exists(local_index):
            print(f"Загрузка обновленного index.html в корень...")
            sftp.put(local_index, "/var/www/charity_web/index.html")
            print("[OK] index.html загружен в корень")
        
        # 2. Убеждаемся что логотип в корневой папке assets
        local_logo = "user_panel/assets/logo.png"
        if os.path.exists(local_logo):
            print(f"Загрузка логотипа в /var/www/charity_web/assets/...")
            client.exec_command("sudo mkdir -p /var/www/charity_web/assets")
            sftp.put(local_logo, "/tmp/logo_final.png")
            client.exec_command("sudo mv /tmp/logo_final.png /var/www/charity_web/assets/logo.png")
            client.exec_command("sudo chmod 644 /var/www/charity_web/assets/logo.png")
            client.exec_command("sudo chown www-data:www-data /var/www/charity_web/assets/logo.png")
            print("[OK] Логотип загружен")
        
        sftp.close()
        
        # 3. Устанавливаем права
        print("Установка прав доступа...")
        client.exec_command("sudo chmod 644 /var/www/charity_web/index.html")
        client.exec_command("sudo chown www-data:www-data /var/www/charity_web/index.html")
        
        # 4. Проверяем что файл правильный
        print("\n--- Проверка загруженного файла ---")
        stdin, stdout, stderr = client.exec_command("head -10 /var/www/charity_web/index.html")
        print(stdout.read().decode())
        
        # 5. Проверяем логотип в файле
        print("\n--- Проверка логотипа в index.html ---")
        stdin, stdout, stderr = client.exec_command("grep -n 'logo.png' /var/www/charity_web/index.html | head -5")
        print(stdout.read().decode())
        
        # 6. Проверяем ссылку #влияние
        print("\n--- Проверка ссылки #влияние ---")
        stdin, stdout, stderr = client.exec_command("grep -n 'влияние' /var/www/charity_web/index.html | head -3")
        print(stdout.read().decode())
        
        # 7. Перезагружаем nginx
        print("\nПерезагрузка nginx...")
        client.exec_command("sudo systemctl reload nginx")
        
        # 8. Проверяем что теперь отдается правильный файл
        print("\n--- Проверка реального ответа сервера ---")
        stdin, stdout, stderr = client.exec_command("curl -s http://localhost/ | head -10")
        actual_response = stdout.read().decode()
        print(actual_response)
        
        # 9. Проверяем логотип в ответе
        print("\n--- Проверка логотипа в ответе ---")
        stdin, stdout, stderr = client.exec_command("curl -s http://localhost/ | grep -i 'logo.png' | head -3")
        logo_check = stdout.read().decode()
        print(logo_check if logo_check else "НЕ НАЙДЕНО!")
        
        client.close()
        
        print("\n" + "="*60)
        print("[SUCCESS] Файлы обновлены в корневой директории!")
        print("="*60)
        print("\n[INFO] Теперь проверьте сайт:")
        print("  https://xn--80adnee0afc6kza.com/")
        print("  https://xn--80adnee0afc6kza.com/#влияние")
        print("\n[INFO] Должны быть видны:")
        print("  - Логотип в navbar")
        print("  - Логотип на главной странице")
        print("  - Favicon в адресной строке")
        print("  - Ссылка #влияние работает")
        print("="*60)
        
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    hostname = 'xn--80adnee0afc6kza.com'
    username = 'root'
    password = 'kxNG6YOk32s0qWNo'
    
    fix_root_index(hostname, username, password)
