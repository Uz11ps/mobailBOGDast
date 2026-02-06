import paramiko
import sys

def add_stories(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # SQL to create table and insert stories
        sql = """
        CREATE TABLE IF NOT EXISTS story (
            id UUID PRIMARY KEY,
            title VARCHAR NOT NULL,
            "imageUrl" VARCHAR NOT NULL,
            caption VARCHAR,
            "createdAt" TIMESTAMP DEFAULT NOW()
        );
        INSERT INTO story (id, title, "imageUrl", caption, "createdAt") VALUES 
        (gen_random_uuid(), 'School in Mali', 'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&q=80&w=800', 'First day at the new school!', NOW()),
        (gen_random_uuid(), 'Clean Water', 'https://images.unsplash.com/photo-1509099836639-18ba1795216d?auto=format&fit=crop&q=80&w=800', '15th well completed.', NOW()),
        (gen_random_uuid(), 'Food for Kids', 'https://images.unsplash.com/photo-1542810634-71277d95dcbb?auto=format&fit=crop&q=80&w=800', '500 hot meals distributed.', NOW());
        """
        
        client.exec_command(f"echo \"{sql}\" > /tmp/stories.sql")
        stdin, stdout, stderr = client.exec_command("sudo -u postgres psql -d charity_db -f /tmp/stories.sql")
        
        print(stdout.read().decode())
        print(stderr.read().decode())

        client.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

add_stories(hostname, username, password)
