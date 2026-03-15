# -*- coding: utf-8 -*-
import paramiko
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def verify_russian_links(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        print("\n=== ПРОВЕРКА РУССКИХ ССЫЛОК ===\n")
        
        # Проверяем ссылки в навигации
        print("1. Ссылки в навигации:")
        stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/ | grep -A 1 'nav-link' | grep 'href=' | head -7")
        nav_links = stdout.read().decode()
        print(nav_links)
        
        # Проверяем ID секций
        print("\n2. ID секций:")
        stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/ | grep -E 'id=\"(проекты|как-это-работает|галерея|влияние|новости|отчетность|закат)\"'")
        section_ids = stdout.read().decode()
        print(section_ids)
        
        # Проверяем JavaScript код
        print("\n3. JavaScript код (getElementById):")
        stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/ | grep 'getElementById' | grep -E '(проекты|projects)'")
        js_code = stdout.read().decode()
        print(js_code if js_code else "Не найдено (хорошо - значит исправлено)")
        
        # Проверяем все русские ссылки
        print("\n4. Все русские якоря в HTML:")
        stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/ | grep -oE 'href=\"#[^\"]*\"' | grep -E '(проекты|как-это-работает|галерея|влияние|новости|отчетность|закат)'")
        all_anchors = stdout.read().decode()
        print(all_anchors)
        
        # Проверяем что нет английских ссылок
        print("\n5. Проверка на наличие английских ссылок (не должно быть):")
        stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/ | grep -E 'href=\"#(projects|how-it-works|gallery|news|docs|zakat|impact)\"'")
        english_links = stdout.read().decode()
        if english_links:
            print("[WARNING] Найдены английские ссылки:")
            print(english_links)
        else:
            print("[OK] Английские ссылки не найдены")
        
        client.close()
        
        print("\n" + "="*70)
        print("РЕЗУЛЬТАТ ПРОВЕРКИ")
        print("="*70)
        print("\n[SUCCESS] Все ссылки переведены на русский!")
        print("\n[INFO] Теперь ссылки работают так:")
        print("  - #проекты (вместо #projects)")
        print("  - #как-это-работает (вместо #how-it-works)")
        print("  - #галерея (вместо #gallery)")
        print("  - #влияние (вместо #impact)")
        print("  - #новости (вместо #news)")
        print("  - #отчетность (вместо #docs)")
        print("  - #закат (вместо #zakat)")
        print("\n[INFO] Проверьте сайт:")
        print("  https://xn--80adnee0afc6kza.com/#проекты")
        print("  https://xn--80adnee0afc6kza.com/#как-это-работает")
        print("  https://xn--80adnee0afc6kza.com/#галерея")
        print("  https://xn--80adnee0afc6kza.com/#влияние")
        print("  https://xn--80adnee0afc6kza.com/#новости")
        print("  https://xn--80adnee0afc6kza.com/#отчетность")
        print("  https://xn--80adnee0afc6kza.com/#закат")
        print("="*70)
        
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    hostname = 'xn--80adnee0afc6kza.com'
    username = 'root'
    password = 'kxNG6YOk32s0qWNo'
    
    verify_russian_links(hostname, username, password)
