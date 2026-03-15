# -*- coding: utf-8 -*-
import paramiko
import sys
import json

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def check_collections(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Подключение к серверу...")
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Проверяем через API
        print("\n=== ПРОВЕРКА ПРОЕКТОВ ИЗ API ===\n")
        stdin, stdout, stderr = client.exec_command("curl -s http://localhost:3000/api/collections | head -50")
        api_response = stdout.read().decode()
        print("Ответ API:")
        print(api_response)
        
        # Пытаемся распарсить JSON
        try:
            collections = json.loads(api_response)
            print("\n=== НАЙДЕННЫЕ ПРОЕКТЫ ===\n")
            for i, c in enumerate(collections, 1):
                print(f"{i}. Заголовок: {c.get('title', 'N/A')}")
                print(f"   Описание: {c.get('description', 'N/A')[:100]}...")
                print(f"   Категория: {c.get('category', 'N/A')}")
                print()
        except:
            print("\n[INFO] Не удалось распарсить JSON, проверяем напрямую в БД...")
            
            # Проверяем в базе данных
            print("\n=== ПРОВЕРКА В БАЗЕ ДАННЫХ ===\n")
            stdin, stdout, stderr = client.exec_command("sudo -u postgres psql -d charity_db -c \"SELECT title, description, category FROM collection LIMIT 5;\"")
            db_result = stdout.read().decode()
            print(db_result)
        
        client.close()
        
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    hostname = 'xn--80adnee0afc6kza.com'
    username = 'root'
    password = 'kxNG6YOk32s0qWNo'
    
    check_collections(hostname, username, password)
