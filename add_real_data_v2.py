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

        # Using a temporary file to avoid shell quoting issues
        sql_content = f"""
        INSERT INTO collection (id, title, description, "goalAmount", "raisedAmount", "imageUrl", category, status, "createdAt", images) VALUES 
        (gen_random_uuid(), 'School Construction in Mali', 'Building a modern school for 300 children.', 1500000, 450000, 'https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&q=80&w=800', 'Школы', 'active', now(), '{school_images}'),
        (gen_random_uuid(), 'Central Mosque in Guinea', 'Helping to complete a spiritual center.', 2500000, 1200000, 'https://images.unsplash.com/photo-1542810634-71277d95dcbb?auto=format&fit=crop&q=80&w=800', 'Мечети', 'active', now(), '{mosque_images}'),
        (gen_random_uuid(), 'Food Basket Program', 'Providing food for families in Niger.', 500000, 320000, 'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&q=80&w=800', 'Питание', 'active', now(), '{food_images}');
        """
        
        with open("temp_data.sql", "w", encoding="utf-8") as f:
            f.write(sql_content)
            
        # Upload temp file
        sftp = client.open_sftp()
        sftp.put("temp_data.sql", "/tmp/temp_data.sql")
        sftp.close()
        
        print("--- Adding real collections from file ---")
        stdin, stdout, stderr = client.exec_command("sudo -u postgres psql -d charity_db -f /tmp/temp_data.sql")
        print(stdout.read().decode())
        print(stderr.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

add_real_collections(hostname, username, password)
