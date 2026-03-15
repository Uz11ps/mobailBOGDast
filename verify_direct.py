# -*- coding: utf-8 -*-
import paramiko
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def verify_direct(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Проверяем строки 227-229 (hero секция)
        print("\n--- Проверка hero секции (строки 227-229) ---")
        stdin, stdout, stderr = client.exec_command("sed -n '227,229p' /var/www/charity_web/user_panel/index.html")
        print(stdout.read().decode())
        
        # Проверяем строки 7-8 (favicon)
        print("\n--- Проверка favicon (строки 7-8) ---")
        stdin, stdout, stderr = client.exec_command("sed -n '7,8p' /var/www/charity_web/user_panel/index.html")
        print(stdout.read().decode())
        
        # Проверяем строку 196 (navbar logo)
        print("\n--- Проверка navbar logo (строка 196) ---")
        stdin, stdout, stderr = client.exec_command("sed -n '196p' /var/www/charity_web/user_panel/index.html")
        print(stdout.read().decode())
        
        client.close()
        
        print("\n[INFO] Все проверки выполнены. Если логотип не виден:")
        print("  - Очистите кэш браузера (Ctrl+Shift+Delete)")
        print("  - Или используйте жесткую перезагрузку (Ctrl+F5)")
        print("  - Или откройте в режиме инкогнито")
        
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    hostname = 'xn--80adnee0afc6kza.com'
    username = 'root'
    password = 'kxNG6YOk32s0qWNo'
    
    verify_direct(hostname, username, password)
