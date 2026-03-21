# -*- coding: utf-8 -*-
import paramiko
import sys
import os

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def force_reload_all(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        sftp = client.open_sftp()
        
        # 1. Загружаем обновленный index.html
        local_index = "user_panel/index.html"
        if os.path.exists(local_index):
            print(f"Загрузка {local_index}...")
            sftp.put(local_index, "/var/www/charity_web/user_panel/index.html")
            print("[OK] index.html загружен")
        
        # 2. Загружаем логотип в корневую папку assets
        local_logo = "user_panel/assets/logo.png"
        if os.path.exists(local_logo):
            print(f"Загрузка логотипа в /var/www/charity_web/assets/...")
            # Создаем папку если её нет
            client.exec_command("sudo mkdir -p /var/www/charity_web/assets")
            sftp.put(local_logo, "/tmp/logo_temp.png")
            client.exec_command("sudo mv /tmp/logo_temp.png /var/www/charity_web/assets/logo.png")
            client.exec_command("sudo chmod 644 /var/www/charity_web/assets/logo.png")
            client.exec_command("sudo chown www-data:www-data /var/www/charity_web/assets/logo.png")
            print("[OK] Логотип загружен")
        
        sftp.close()
        
        # 3. Проверяем hero секцию
        print("\n--- Проверка hero секции с логотипом ---")
        stdin, stdout, stderr = client.exec_command("grep -A 5 'hero-title\\|НОВАЯ ЖИЗНЬ' /var/www/charity_web/user_panel/index.html | head -15")
        print(stdout.read().decode())
        
        # 4. Устанавливаем правильные права
        print("\nУстановка прав доступа...")
        client.exec_command("sudo chmod 644 /var/www/charity_web/user_panel/index.html")
        client.exec_command("sudo chown www-data:www-data /var/www/charity_web/user_panel/index.html")
        
        # 5. Очищаем кэш nginx (если есть)
        print("Очистка кэша...")
        client.exec_command("sudo systemctl reload nginx")
        
        # 6. Проверяем финальное состояние
        print("\n--- Финальная проверка ---")
        stdin, stdout, stderr = client.exec_command("grep -n 'logo.png' /var/www/charity_web/user_panel/index.html")
        print(stdout.read().decode())
        
        stdin, stdout, stderr = client.exec_command("ls -la /var/www/charity_web/assets/logo.png")
        print(stdout.read().decode())
        
        client.close()
        
        print("\n" + "="*60)
        print("[SUCCESS] Все файлы перезагружены!")
        print("="*60)
        print("\n[ВАЖНО] Для просмотра изменений:")
        print("  1. Очистите кэш браузера: Ctrl+Shift+Delete или Ctrl+F5")
        print("  2. Или откройте сайт в режиме инкогнито")
        print("  3. Или добавьте ?v=2 в конец URL для обхода кэша")
        print("\n[INFO] Проверьте:")
        print("  - Логотип в navbar (слева от 'НОВАЯ ЖИЗНЬ')")
        print("  - Логотип на главной странице (в hero секции)")
        print("  - Favicon в адресной строке браузера")
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
    
    force_reload_all(hostname, username, password)
