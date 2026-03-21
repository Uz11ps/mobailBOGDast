import paramiko
import sys

def add_real_collections(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        school_images = "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&q=80&w=800"
        mosque_images = "https://images.unsplash.com/photo-1542810634-71277d95dcbb?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1564769625905-50e93615e769?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1591604129939-f1efa4d9f7fa?auto=format&fit=crop&q=80&w=800"
        food_images = "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1593113598332-cd288d649433?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1532629345422-7515f3d16bb8?auto=format&fit=crop&q=80&w=800"

        sql = f"""
        INSERT INTO collection (id, title, description, "goalAmount", "raisedAmount", "imageUrl", category, status, "createdAt", images) VALUES 
        (gen_random_uuid(), 'Строительство школы в Мали', 'Мы строим современную школу для 300 детей, которые сейчас вынуждены учиться под открытым небом.', 1500000, 450000, 'https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&q=80&w=800', 'Школы', 'active', now(), '{school_images}'),
        (gen_random_uuid(), 'Центральная мечеть в Гвинее', 'Помогите завершить строительство духовного центра, который станет местом объединения для всей общины.', 2500000, 1200000, 'https://images.unsplash.com/photo-1542810634-71277d95dcbb?auto=format&fit=crop&q=80&w=800', 'Мечети', 'active', now(), '{mosque_images}'),
        (gen_random_uuid(), 'Продовольственная корзина', 'Обеспечение продуктами питания семей, пострадавших от засухи в Нигере.', 500000, 320000, 'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&q=80&w=800', 'Питание', 'active', now(), '{food_images}');
        """
        
        print("--- Adding real collections ---")
        stdin, stdout, stderr = client.exec_command(f"sudo -u postgres psql -d charity_db -c \"{sql}\"")
        print(stdout.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

add_real_collections(hostname, username, password)
