import paramiko
import sys

def populate_partners(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        sql = """
        INSERT INTO partner (id, name, "logoUrl", "websiteUrl", "createdAt") VALUES 
        (gen_random_uuid(), 'UNICEF', 'https://upload.wikimedia.org/wikipedia/commons/c/c1/UNICEF_Logo.svg', 'https://www.unicef.org', now()),
        (gen_random_uuid(), 'Red Cross', 'https://upload.wikimedia.org/wikipedia/commons/a/ad/Red_Cross_logo.svg', 'https://www.icrc.org', now()),
        (gen_random_uuid(), 'Nouvelle Vie', 'https://upload.wikimedia.org/wikipedia/en/thumb/c/c3/Nouvelle_Vie_Logo.png/220px-Nouvelle_Vie_Logo.png', 'https://nouvellevie.fr', now()),
        (gen_random_uuid(), 'WFP', 'https://upload.wikimedia.org/wikipedia/commons/4/41/WFP_Logo.svg', 'https://www.wfp.org', now());
        """
        
        with open("partners.sql", "w", encoding="utf-8") as f:
            f.write(sql)
            
        sftp = client.open_sftp()
        sftp.put("partners.sql", "/tmp/partners.sql")
        sftp.close()
        
        print("--- Executing partners SQL ---")
        stdin, stdout, stderr = client.exec_command("sudo -u postgres psql -d charity_db -f /tmp/partners.sql")
        print(stdout.read().decode())
        print(stderr.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

populate_partners(hostname, username, password)
