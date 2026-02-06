import paramiko
import sys

def fix_db_columns(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # SQL to fix column names (TypeORM expects camelCase in quotes or snake_case depending on config)
        # Looking at the SELECT output, it has "imageurl" and "createdat" (all lowercase)
        # But TypeORM entity has "imageUrl" and "createdAt"
        
        sql = """
        ALTER TABLE story RENAME COLUMN imageurl TO "imageUrl";
        ALTER TABLE story RENAME COLUMN createdat TO "createdAt";
        """
        
        cmd = f"sudo -u postgres psql -d charity_db -c '{sql}'"
        stdin, stdout, stderr = client.exec_command(cmd)
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

fix_db_columns(hostname, username, password)
