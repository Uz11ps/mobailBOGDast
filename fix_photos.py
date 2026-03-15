import paramiko
import sys

def fix_categories_and_photos(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Check current categories
        print("--- Current categories in DB ---")
        stdin, stdout, stderr = client.exec_command("sudo -u postgres psql -d charity_db -c 'SELECT DISTINCT category FROM collection;'")
        print(stdout.read().decode())

        # Update categories to match the ones used in the app/web
        # And set multi-photos
        
        school_images = "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&q=80&w=800"
        mosque_images = "https://images.unsplash.com/photo-1542810634-71277d95dcbb?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1564769625905-50e93615e769?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1591604129939-f1efa4d9f7fa?auto=format&fit=crop&q=80&w=800"
        food_images = "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1593113598332-cd288d649433?auto=format&fit=crop&q=80&w=800,https://images.unsplash.com/photo-1532629345422-7515f3d16bb8?auto=format&fit=crop&q=80&w=800"

        sql = f"""
        UPDATE collection SET category = 'Школы', images = '{school_images}' WHERE title ILIKE '%школ%';
        UPDATE collection SET category = 'Мечети', images = '{mosque_images}' WHERE title ILIKE '%мечет%';
        UPDATE collection SET category = 'Питание', images = '{food_images}' WHERE title ILIKE '%еда%' OR title ILIKE '%пит%';
        UPDATE collection SET images = '{school_images}' WHERE images IS NULL OR images = '';
        """
        
        print("--- Fixing categories and photos ---")
        stdin, stdout, stderr = client.exec_command(f"sudo -u postgres psql -d charity_db -c \"{sql}\"")
        print(stdout.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

fix_categories_and_photos(hostname, username, password)
