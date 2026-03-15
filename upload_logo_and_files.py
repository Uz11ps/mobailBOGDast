# -*- coding: utf-8 -*-
import paramiko
import os
import sys
from pathlib import Path

# Устанавливаем кодировку для Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def upload_files(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Открываем SFTP соединение
        sftp = client.open_sftp()
        
        # 1. Создаем папку assets на сервере если её нет
        print("Создание папки assets на сервере...")
        stdin, stdout, stderr = client.exec_command("mkdir -p /var/www/charity_web/user_panel/assets")
        stdout.channel.recv_exit_status()
        
        # 2. Загружаем логотип
        local_logo_path = "user_panel/assets/logo.png"
        remote_logo_path = "/var/www/charity_web/user_panel/assets/logo.png"
        
        if os.path.exists(local_logo_path):
            print(f"Загрузка логотипа: {local_logo_path} -> {remote_logo_path}")
            sftp.put(local_logo_path, remote_logo_path)
            print("[OK] Логотип загружен")
        else:
            print(f"[WARNING] Файл {local_logo_path} не найден локально")
        
        # 3. Загружаем обновленный index.html
        local_index_path = "user_panel/index.html"
        remote_index_path = "/var/www/charity_web/user_panel/index.html"
        
        if os.path.exists(local_index_path):
            print(f"Загрузка index.html: {local_index_path} -> {remote_index_path}")
            sftp.put(local_index_path, remote_index_path)
            print("[OK] index.html загружен")
        else:
            print(f"⚠ Файл {local_index_path} не найден локально")
        
        # 4. Устанавливаем правильные права доступа
        print("Установка прав доступа...")
        client.exec_command("chmod 644 /var/www/charity_web/user_panel/index.html")
        client.exec_command("chmod 644 /var/www/charity_web/user_panel/assets/logo.png")
        client.exec_command("chown -R www-data:www-data /var/www/charity_web/user_panel/")
        
        # 5. Проверяем что файлы загружены
        print("\n--- Проверка загруженных файлов ---")
        stdin, stdout, stderr = client.exec_command("ls -la /var/www/charity_web/user_panel/assets/")
        print(stdout.read().decode())
        
        stdin, stdout, stderr = client.exec_command("ls -la /var/www/charity_web/user_panel/index.html")
        print(stdout.read().decode())
        
        sftp.close()
        client.close()
        
        print("\n[SUCCESS] Все файлы успешно загружены на сервер!")
        print("[INFO] Проверьте сайт: https://xn--80adnee0afc6kza.com/")
        print("[TIP] Если изменения не видны, очистите кэш браузера (Ctrl+F5)")
        
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    hostname = 'xn--80adnee0afc6kza.com'
    username = 'root'
    password = 'kxNG6YOk32s0qWNo'
    
    upload_files(hostname, username, password)
