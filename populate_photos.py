import paramiko
import sys

def populate_multi_photos(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # 1. Add 'images' column to 'collection' table
        print("--- Adding 'images' column to collection table ---")
        stdin, stdout, stderr = client.exec_command("sudo -u postgres psql -d charity_db -c 'ALTER TABLE collection ADD COLUMN IF NOT EXISTS images text;'")
        print(stdout.read().decode())
        
        # 2. Update existing collections with sample multi-photos
        # We'll use high-quality unsplash images for schools, mosques, and food
        
        # School images
        school_images = "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&q=80&w=800"
        
        # Mosque images
        mosque_images = "https://images.unsplash.com/photo-1542810634-71277d95dcbb?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1564769625905-50e93615e769?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1591604129939-f1efa4d9f7fa?auto=format&fit=crop&q=80&w=800"
        
        # Food images
        food_images = "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1593113598332-cd288d649433?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1532629345422-7515f3d16bb8?auto=format&fit=crop&q=80&w=800"

        sql = f"""
        UPDATE collection SET images = '{school_images}' WHERE category = 'Школы';
        UPDATE collection SET images = '{mosque_images}' WHERE category = 'Мечети';
        UPDATE collection SET images = '{food_images}' WHERE category = 'Питание';
        UPDATE collection SET images = '{school_images}' WHERE images IS NULL;
        """
        
        print("--- Updating collections with multi-photos ---")
        stdin, stdout, stderr = client.exec_command(f"sudo -u postgres psql -d charity_db -c \"{sql}\"")
        print(stdout.read().decode())
        print(stderr.read().decode())

        # 3. Add more Gallery Items to make it look full
        print("--- Populating Gallery with more items ---")
        gallery_sql = """
        INSERT INTO gallery_item (id, "imageUrl", title, country, category, "createdAt") VALUES 
        (gen_random_uuid(), 'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&q=80&w=800', 'Счастливые дети', 'Мали', 'Африка', now()),
        (gen_random_uuid(), 'https://images.unsplash.com/photo-1509099836639-18ba1795216d?auto=format&fit=crop&q=80&w=800', 'Новый колодец', 'Нигер', 'Африка', now()),
        (gen_random_uuid(), 'https://images.unsplash.com/photo-1542810634-71277d95dcbb?auto=format&fit=crop&q=80&w=800', 'Строительство мечети', 'Гвинея', 'Африка', now()),
        (gen_random_uuid(), 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&q=80&w=800', 'Урок в новой школе', 'Мали', 'Африка', now()),
        (gen_random_uuid(), 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&q=80&w=800', 'Библиотека', 'Нигер', 'Африка', now()),
        (gen_random_uuid(), 'https://images.unsplash.com/photo-1591604129939-f1efa4d9f7fa?auto=format&fit=crop&q=80&w=800', 'Вечерняя молитва', 'Турция', 'Азия', now()),
        (gen_random_uuid(), 'https://images.unsplash.com/photo-1532629345422-7515f3d16bb8?auto=format&fit=crop&q=80&w=800', 'Раздача еды', 'Палестина', 'Азия', now()),
        (gen_random_uuid(), 'https://images.unsplash.com/photo-1593113598332-cd288d649433?auto=format&fit=crop&q=80&w=800', 'Помощь семьям', 'Сирия', 'Азия', now());
        """
        stdin, stdout, stderr = client.exec_command(f"sudo -u postgres psql -d charity_db -c \"{gallery_sql}\"")
        print(stdout.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

populate_multi_photos(hostname, username, password)
