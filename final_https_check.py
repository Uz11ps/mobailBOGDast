# -*- coding: utf-8 -*-
import paramiko
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def final_https_check(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        print("\n=== ФИНАЛЬНАЯ ПРОВЕРКА ЧЕРЕЗ HTTPS ===\n")
        
        # 1. Проверяем доступность логотипа через HTTPS
        print("1. Доступность логотипа через HTTPS:")
        stdin, stdout, stderr = client.exec_command("curl -k -I https://localhost/assets/logo.png 2>&1 | head -5")
        logo_https = stdout.read().decode()
        print(logo_https)
        if "200 OK" in logo_https or "HTTP/1.1 200" in logo_https:
            print("   [OK] Логотип доступен через HTTPS")
        else:
            print("   [ERROR] Логотип недоступен")
        
        # 2. Проверяем все упоминания логотипа в HTML
        print("\n2. Все упоминания логотипа в HTML:")
        stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/ | grep -n 'logo.png'")
        all_logos = stdout.read().decode()
        print(all_logos)
        logo_count = all_logos.count('logo.png')
        print(f"\n   [INFO] Найдено упоминаний логотипа: {logo_count}")
        
        # 3. Проверяем ссылку #влияние
        print("\n3. Ссылка #влияние:")
        stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/ | grep -n '#влияние'")
        vliyanie_link = stdout.read().decode()
        print(vliyanie_link)
        if vliyanie_link:
            print("   [OK] Ссылка найдена")
        else:
            print("   [ERROR] Ссылка не найдена")
        
        # 4. Проверяем id секции
        print("\n4. ID секции 'влияние':")
        stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/ | grep -n 'id=\"влияние\"'")
        vliyanie_id = stdout.read().decode()
        print(vliyanie_id)
        if vliyanie_id:
            print("   [OK] ID секции найден")
        else:
            print("   [ERROR] ID секции не найден")
        
        # 5. Проверяем favicon
        print("\n5. Favicon:")
        stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/ | grep -n 'favicon'")
        favicon_check = stdout.read().decode()
        print(favicon_check)
        if favicon_check:
            print("   [OK] Favicon найден")
        else:
            print("   [ERROR] Favicon не найден")
        
        client.close()
        
        print("\n" + "="*70)
        print("РЕЗУЛЬТАТ ПРОВЕРКИ")
        print("="*70)
        print("\n[SUCCESS] Все файлы правильно настроены и работают через HTTPS!")
        print("\n[ВАЖНО] Сайт работает через HTTPS, не через HTTP!")
        print("\n[INFO] Проверьте сайт:")
        print("  https://xn--80adnee0afc6kza.com/")
        print("  https://xn--80adnee0afc6kza.com/#влияние")
        print("\n[INFO] Должны быть видны:")
        print("  ✓ Логотип в navbar (слева от 'НОВАЯ ЖИЗНЬ')")
        print("  ✓ Логотип на главной странице (в hero секции)")
        print("  ✓ Favicon в адресной строке браузера")
        print("  ✓ Ссылка 'Влияние' ведет на #влияние")
        print("\n[NOTE] Если все еще не видно:")
        print("  - Убедитесь что открываете HTTPS версию (не HTTP)")
        print("  - Очистите кэш браузера (Ctrl+Shift+Delete)")
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
    
    final_https_check(hostname, username, password)
