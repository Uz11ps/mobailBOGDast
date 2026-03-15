
        UPDATE collection SET "imageUrl" = 'https://xn--80adnee0afc6kza.com/uploads/image0.jpeg', images = 'https://xn--80adnee0afc6kza.com/uploads/image0.jpeg,https://xn--80adnee0afc6kza.com/uploads/image1.jpeg,https://xn--80adnee0afc6kza.com/uploads/image2.jpeg' WHERE category = 'Школы';
        UPDATE collection SET "imageUrl" = 'https://xn--80adnee0afc6kza.com/uploads/image10.jpeg', images = 'https://xn--80adnee0afc6kza.com/uploads/image10.jpeg,https://xn--80adnee0afc6kza.com/uploads/image11.jpeg,https://xn--80adnee0afc6kza.com/uploads/image12.jpeg' WHERE category = 'Мечети';
        UPDATE collection SET "imageUrl" = 'https://xn--80adnee0afc6kza.com/uploads/image20.jpeg', images = 'https://xn--80adnee0afc6kza.com/uploads/image20.jpeg,https://xn--80adnee0afc6kza.com/uploads/image21.jpeg,https://xn--80adnee0afc6kza.com/uploads/image22.jpeg' WHERE category = 'Питание';
        
        DELETE FROM gallery_item;
        INSERT INTO gallery_item (id, "imageUrl", title, country, category, "createdAt") VALUES 
        (gen_random_uuid(), 'https://xn--80adnee0afc6kza.com/uploads/image3.jpeg', 'Наши подопечные', 'Мали', 'Африка', now()),
        (gen_random_uuid(), 'https://xn--80adnee0afc6kza.com/uploads/image4.jpeg', 'Строительство', 'Нигер', 'Африка', now()),
        (gen_random_uuid(), 'https://xn--80adnee0afc6kza.com/uploads/image5.jpeg', 'Радость детей', 'Гвинея', 'Африка', now()),
        (gen_random_uuid(), 'https://xn--80adnee0afc6kza.com/uploads/image6.jpeg', 'Новая школа', 'Мали', 'Африка', now()),
        (gen_random_uuid(), 'https://xn--80adnee0afc6kza.com/uploads/image7.jpeg', 'Чистая вода', 'Нигер', 'Африка', now()),
        (gen_random_uuid(), 'https://xn--80adnee0afc6kza.com/uploads/image13.jpeg', 'Мечеть изнутри', 'Турция', 'Азия', now()),
        (gen_random_uuid(), 'https://xn--80adnee0afc6kza.com/uploads/image14.jpeg', 'Помощь семьям', 'Палестина', 'Азия', now()),
        (gen_random_uuid(), 'https://xn--80adnee0afc6kza.com/uploads/image15.jpeg', 'Урок Корана', 'Сирия', 'Азия', now()),
        (gen_random_uuid(), 'https://xn--80adnee0afc6kza.com/uploads/image23.jpeg', 'Обед для всех', 'Мали', 'Африка', now()),
        (gen_random_uuid(), 'https://xn--80adnee0afc6kza.com/uploads/image24.jpeg', 'Фундамент будущего', 'Нигер', 'Африка', now()),
        (gen_random_uuid(), 'https://xn--80adnee0afc6kza.com/uploads/image25.jpeg', 'Улыбки', 'Гвинея', 'Африка', now()),
        (gen_random_uuid(), 'https://xn--80adnee0afc6kza.com/uploads/image26.jpeg', 'Завершение работ', 'Мали', 'Африка', now());
        
        UPDATE news SET "imageUrl" = 'https://xn--80adnee0afc6kza.com/uploads/image30.jpeg' WHERE title LIKE '%школ%';
        UPDATE news SET "imageUrl" = 'https://xn--80adnee0afc6kza.com/uploads/image31.jpeg' WHERE title LIKE '%миссия%';
        UPDATE news SET "imageUrl" = 'https://xn--80adnee0afc6kza.com/uploads/image32.jpeg' WHERE title LIKE '%колодцев%';
        
        UPDATE story SET "imageUrl" = 'https://xn--80adnee0afc6kza.com/uploads/image17.jpeg' WHERE title = 'School in Mali';
        UPDATE story SET "imageUrl" = 'https://xn--80adnee0afc6kza.com/uploads/image18.jpeg' WHERE title = 'Clean Water';
        UPDATE story SET "imageUrl" = 'https://xn--80adnee0afc6kza.com/uploads/image19.jpeg' WHERE title = 'Food for Kids';
        