import paramiko
import sys

def update_db_with_local_images(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, timeout=60)
        
        # Base URL for uploaded images
        base_url = "https://xn--80adnee0afc6kza.com/uploads/"
        
        # 1. Update Collections
        # We'll assign specific images to collections
        school_images = f"{base_url}image0.jpeg,{base_url}image1.jpeg,{base_url}image2.jpeg"
        mosque_images = f"{base_url}image10.jpeg,{base_url}image11.jpeg,{base_url}image12.jpeg"
        food_images = f"{base_url}image20.jpeg,{base_url}image21.jpeg,{base_url}image22.jpeg"
        
        sql = f"""
        UPDATE collection SET "imageUrl" = '{base_url}image0.jpeg', images = '{school_images}' WHERE category = 'Школы';
        UPDATE collection SET "imageUrl" = '{base_url}image10.jpeg', images = '{mosque_images}' WHERE category = 'Мечети';
        UPDATE collection SET "imageUrl" = '{base_url}image20.jpeg', images = '{food_images}' WHERE category = 'Питание';
        """
        
        # 2. Update Gallery Items
        gallery_sql = f"""
        DELETE FROM gallery_item;
        INSERT INTO gallery_item (id, "imageUrl", title, country, category, "createdAt") VALUES 
        (gen_random_uuid(), '{base_url}image3.jpeg', 'Наши подопечные', 'Мали', 'Африка', now()),
        (gen_random_uuid(), '{base_url}image4.jpeg', 'Строительство', 'Нигер', 'Африка', now()),
        (gen_random_uuid(), '{base_url}image5.jpeg', 'Радость детей', 'Гвинея', 'Африка', now()),
        (gen_random_uuid(), '{base_url}image6.jpeg', 'Новая школа', 'Мали', 'Африка', now()),
        (gen_random_uuid(), '{base_url}image7.jpeg', 'Чистая вода', 'Нигер', 'Африка', now()),
        (gen_random_uuid(), '{base_url}image13.jpeg', 'Мечеть изнутри', 'Турция', 'Азия', now()),
        (gen_random_uuid(), '{base_url}image14.jpeg', 'Помощь семьям', 'Палестина', 'Азия', now()),
        (gen_random_uuid(), '{base_url}image15.jpeg', 'Урок Корана', 'Сирия', 'Азия', now()),
        (gen_random_uuid(), '{base_url}image23.jpeg', 'Обед для всех', 'Мали', 'Африка', now()),
        (gen_random_uuid(), '{base_url}image24.jpeg', 'Фундамент будущего', 'Нигер', 'Африка', now()),
        (gen_random_uuid(), '{base_url}image25.jpeg', 'Улыбки', 'Гвинея', 'Африка', now()),
        (gen_random_uuid(), '{base_url}image26.jpeg', 'Завершение работ', 'Мали', 'Африка', now());
        """

        # 3. Update News
        news_sql = f"""
        UPDATE news SET "imageUrl" = '{base_url}image30.jpeg' WHERE title LIKE '%школ%';
        UPDATE news SET "imageUrl" = '{base_url}image31.jpeg' WHERE title LIKE '%миссия%';
        UPDATE news SET "imageUrl" = '{base_url}image32.jpeg' WHERE title LIKE '%колодцев%';
        """

        # 4. Update Stories
        stories_sql = f"""
        UPDATE story SET "imageUrl" = '{base_url}image17.jpeg' WHERE title = 'School in Mali';
        UPDATE story SET "imageUrl" = '{base_url}image18.jpeg' WHERE title = 'Clean Water';
        UPDATE story SET "imageUrl" = '{base_url}image19.jpeg' WHERE title = 'Food for Kids';
        """

        full_sql = sql + gallery_sql + news_sql + stories_sql
        
        with open("update_with_local.sql", "w", encoding="utf-8") as f:
            f.write(full_sql)
            
        sftp = client.open_sftp()
        sftp.put("update_with_local.sql", "/tmp/update_with_local.sql")
        sftp.close()
        
        print("--- Executing update with local images SQL ---")
        stdin, stdout, stderr = client.exec_command("sudo -u postgres psql -d charity_db -f /tmp/update_with_local.sql")
        print(stdout.read().decode())
        print(stderr.read().decode())

        client.close()
    except Exception as e:
        print(f"Error: {e}")

hostname = 'xn--80adnee0afc6kza.com'
username = 'root'
password = 'kxNG6YOk32s0qWNo'

update_db_with_local_images(hostname, username, password)
