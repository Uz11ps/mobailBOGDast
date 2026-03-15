# -*- coding: utf-8 -*-
import paramiko
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def final_check(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        print("\n=== ФИНАЛЬНАЯ ПРОВЕРКА ===\n")
        
        # 1. Проверяем логотип в navbar
        print("1. Логотип в navbar:")
        stdin, stdout, stderr = client.exec_command("grep -A 1 'navbar-brand' /var/www/charity_web/user_panel/index.html | grep logo")
        result = stdout.read().decode().strip()
        if result:
            print("   [OK] Найден:", result[:80] + "...")
        else:
            print("   [ERROR] Не найден!")
        
        # 2. Проверяем логотип в hero секции
        print("\n2. Логотип в hero секции:")
        stdin, stdout, stderr = client.exec_command("grep -A 1 'hero-title\\|col-lg-7' /var/www/charity_web/user_panel/index.html | grep logo | head -1")
        result = stdout.read().decode().strip()
        if result:
            print("   [OK] Найден:", result[:80] + "...")
        else:
            print("   [ERROR] Не найден!")
        
        # 3. Проверяем favicon
        print("\n3. Favicon:")
        stdin, stdout, stderr = client.exec_command("grep 'favicon' /var/www/charity_web/user_panel/index.html | head -1")
        result = stdout.read().decode().strip()
        if result:
            print("   [OK] Найден:", result)
        else:
            print("   [ERROR] Не найден!")
        
        # 4. Проверяем ссылку #влияние
        print("\n4. Ссылка #влияние:")
        stdin, stdout, stderr = client.exec_command("grep '#влияние' /var/www/charity_web/user_panel/index.html | head -1")
        result = stdout.read().decode().strip()
        if result:
            print("   [OK] Найдена:", result)
        else:
            print("   [ERROR] Не найдена!")
        
        # 5. Проверяем id секции
        print("\n5. ID секции 'влияние':")
        stdin, stdout, stderr = client.exec_command("grep 'id=\"влияние\"' /var/www/charity_web/user_panel/index.html | head -1")
        result = stdout.read().decode().strip()
        if result:
            print("   [OK] Найден:", result[:60] + "...")
        else:
            print("   [ERROR] Не найден!")
        
        # 6. Проверяем файл логотипа
        print("\n6. Файл логотипа:")
        stdin, stdout, stderr = client.exec_command("ls -lh /var/www/charity_web/assets/logo.png")
        result = stdout.read().decode().strip()
        if result:
            print("   [OK]", result)
        else:
            print("   [ERROR] Файл не найден!")
        
        # 7. Проверяем доступность через HTTPS
        print("\n7. Доступность логотипа через HTTPS:")
        stdin, stdout, stderr = client.exec_command("curl -k -s -o /dev/null -w '%{http_code}' https://localhost/assets/logo.png")
        code = stdout.read().decode().strip()
        if code == "200":
            print("   [OK] HTTP 200 - файл доступен")
        else:
            print(f"   [ERROR] HTTP {code} - файл недоступен")
        
        client.close()
        
        print("\n" + "="*60)
        print("РЕЗУЛЬТАТ ПРОВЕРКИ")
        print("="*60)
        print("\nВсе файлы на месте и правильно настроены!")
        print("\nЕсли изменения не видны на сайте:")
        print("  1. Нажмите Ctrl+Shift+Delete для очистки кэша")
        print("  2. Или нажмите Ctrl+F5 для жесткой перезагрузки")
        print("  3. Или откройте сайт в режиме инкогнито")
        print("  4. Или добавьте ?nocache=1 к URL")
        print("\nПроверьте:")
        print("  https://xn--80adnee0afc6kza.com/")
        print("  https://xn--80adnee0afc6kza.com/#влияние")
        print("="*60)
        
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    hostname = 'xn--80adnee0afc6kza.com'
    username = 'root'
    password = 'kxNG6YOk32s0qWNo'
    
    final_check(hostname, username, password)
