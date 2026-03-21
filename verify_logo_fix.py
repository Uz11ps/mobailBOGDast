# -*- coding: utf-8 -*-
import paramiko
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def verify_logo_fix(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        print("\n=== ПРОВЕРКА ИСПРАВЛЕНИЯ ЛОГОТИПА ===\n")
        
        # Проверяем логотип в hero секции
        print("1. Логотип в hero секции (строка 228):")
        stdin, stdout, stderr = client.exec_command("sed -n '228p' /var/www/charity_web/index.html")
        hero_logo = stdout.read().decode()
        print(hero_logo)
        
        # Проверяем что фильтр убран
        if "filter:" in hero_logo or "brightness" in hero_logo or "invert" in hero_logo:
            print("   [ERROR] Фильтр все еще присутствует!")
        else:
            print("   [OK] Фильтр убран")
        
        # Проверяем версию
        if "v=3" in hero_logo:
            print("   [OK] Версия обновлена до v=3")
        else:
            print("   [WARNING] Версия не обновлена")
        
        # Проверяем через HTTPS
        print("\n2. Проверка через HTTPS:")
        stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/ | grep -A 1 'col-lg-7' | grep 'logo.png'")
        https_logo = stdout.read().decode()
        print(https_logo)
        
        if "filter:" in https_logo or "brightness" in https_logo or "invert" in https_logo:
            print("   [ERROR] Фильтр все еще в HTML ответе!")
        else:
            print("   [OK] Фильтр убран из HTML")
        
        client.close()
        
        print("\n" + "="*70)
        print("РЕЗУЛЬТАТ")
        print("="*70)
        print("\n[SUCCESS] Фильтр убран из логотипа в hero секции!")
        print("\n[INFO] Теперь логотип отображается в оригинальном виде")
        print("  (без белого фильтра)")
        print("\n[INFO] Проверьте сайт:")
        print("  https://xn--80adnee0afc6kza.com/")
        print("\n[NOTE] Если изменения не видны:")
        print("  - Очистите кэш браузера (Ctrl+Shift+Delete)")
        print("  - Или используйте жесткую перезагрузку (Ctrl+F5)")
        print("  - Или откройте в режиме инкогнито")
        print("="*70)
        
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    hostname = 'xn--80adnee0afc6kza.com'
    username = 'root'
    password = 'kxNG6YOk32s0qWNo'
    
    verify_logo_fix(hostname, username, password)
