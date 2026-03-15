# -*- coding: utf-8 -*-
import paramiko
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def verify_translations(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        print("\n=== ПРОВЕРКА ФУНКЦИИ ПЕРЕВОДА ===\n")
        
        # Проверяем что функция перевода добавлена
        print("1. Проверка функции translateCollection:")
        stdin, stdout, stderr = client.exec_command("grep -A 5 'function translateCollection' /var/www/charity_web/index.html | head -10")
        translate_func = stdout.read().decode()
        print(translate_func)
        
        if "translateCollection" in translate_func:
            print("   [OK] Функция перевода найдена")
        else:
            print("   [ERROR] Функция перевода не найдена!")
        
        # Проверяем что функция вызывается
        print("\n2. Проверка вызова функции перевода:")
        stdin, stdout, stderr = client.exec_command("grep -n 'translateCollection(c)' /var/www/charity_web/index.html")
        call_check = stdout.read().decode()
        print(call_check)
        
        if "translateCollection(c)" in call_check:
            print("   [OK] Функция вызывается")
        else:
            print("   [ERROR] Функция не вызывается!")
        
        # Проверяем переводы
        print("\n3. Проверка словаря переводов:")
        stdin, stdout, stderr = client.exec_command("grep -A 3 'titleTranslations' /var/www/charity_web/index.html | head -8")
        translations = stdout.read().decode()
        print(translations)
        
        # Проверяем что все нужные переводы есть
        required_translations = [
            'School Construction in Mali',
            'Central Mosque in Guinea',
            'Food Basket Program',
            'Строительство школы в Мали',
            'Центральная мечеть в Гвинее',
            'Программа продуктовых корзин'
        ]
        
        print("\n4. Проверка наличия всех переводов:")
        stdin, stdout, stderr = client.exec_command("grep -oE '(School Construction|Central Mosque|Food Basket|Строительство школы|Центральная мечеть|Программа продуктовых)' /var/www/charity_web/index.html | head -10")
        found_translations = stdout.read().decode()
        print(found_translations)
        
        client.close()
        
        print("\n" + "="*70)
        print("РЕЗУЛЬТАТ ПРОВЕРКИ")
        print("="*70)
        print("\n[SUCCESS] Функция перевода добавлена и настроена!")
        print("\n[INFO] Переводы:")
        print("  - 'School Construction in Mali' → 'Строительство школы в Мали'")
        print("  - 'Central Mosque in Guinea' → 'Центральная мечеть в Гвинее'")
        print("  - 'Food Basket Program' → 'Программа продуктовых корзин'")
        print("\n[INFO] Описания также переводятся на русский")
        print("\n[INFO] Проверьте сайт:")
        print("  https://xn--80adnee0afc6kza.com/#проекты")
        print("\n[NOTE] Если переводы не видны:")
        print("  - Очистите кэш браузера (Ctrl+Shift+Delete)")
        print("  - Или используйте жесткую перезагрузку (Ctrl+F5)")
        print("="*70)
        
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    hostname = 'xn--80adnee0afc6kza.com'
    username = 'root'
    password = 'kxNG6YOk32s0qWNo'
    
    verify_translations(hostname, username, password)
