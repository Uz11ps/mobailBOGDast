
        DELETE FROM gallery_item WHERE title = '123';
        INSERT INTO gallery_item (id, "imageUrl", title, country, category, "createdAt") VALUES 
        (gen_random_uuid(), 'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&q=80&w=800', 'Счастливые дети', 'Мали', 'Африка', now()),
        (gen_random_uuid(), 'https://images.unsplash.com/photo-1509099836639-18ba1795216d?auto=format&fit=crop&q=80&w=800', 'Новый колодец', 'Нигер', 'Африка', now()),
        (gen_random_uuid(), 'https://images.unsplash.com/photo-1542810634-71277d95dcbb?auto=format&fit=crop&q=80&w=800', 'Строительство мечети', 'Гвинея', 'Африка', now()),
        (gen_random_uuid(), 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&q=80&w=800', 'Урок в новой школе', 'Мали', 'Африка', now()),
        (gen_random_uuid(), 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&q=80&w=800', 'Библиотека', 'Нигер', 'Африка', now()),
        (gen_random_uuid(), 'https://images.unsplash.com/photo-1591604129939-f1efa4d9f7fa?auto=format&fit=crop&q=80&w=800', 'Вечерняя молитва', 'Турция', 'Азия', now()),
        (gen_random_uuid(), 'https://images.unsplash.com/photo-1532629345422-7515f3d16bb8?auto=format&fit=crop&q=80&w=800', 'Раздача еды', 'Палестина', 'Азия', now()),
        (gen_random_uuid(), 'https://images.unsplash.com/photo-1593113598332-cd288d649433?auto=format&fit=crop&q=80&w=800', 'Помощь семьям', 'Сирия', 'Азия', now());
        
        INSERT INTO news (id, title, content, "imageUrl", "createdAt") VALUES 
        (gen_random_uuid(), 'Открытие новой школы в Мали', 'Сегодня мы официально открыли двери новой школы для 300 детей. Это стало возможным благодаря вашим пожертвованиям.', 'https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&q=80&w=800', now()),
        (gen_random_uuid(), 'Гуманитарная миссия в Нигере', 'Наша команда доставила более 500 продовольственных корзин в отдаленные районы Нигера.', 'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&q=80&w=800', now()),
        (gen_random_uuid(), 'Завершение строительства колодцев', '15 новых колодцев теперь обеспечивают чистой водой более 5000 человек.', 'https://images.unsplash.com/photo-1509099836639-18ba1795216d?auto=format&fit=crop&q=80&w=800', now());
        DELETE FROM collection WHERE title = '123';