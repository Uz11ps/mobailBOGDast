
        INSERT INTO partner (id, name, "logoUrl", "websiteUrl", "createdAt") VALUES 
        (gen_random_uuid(), 'UNICEF', 'https://upload.wikimedia.org/wikipedia/commons/c/c1/UNICEF_Logo.svg', 'https://www.unicef.org', now()),
        (gen_random_uuid(), 'Red Cross', 'https://upload.wikimedia.org/wikipedia/commons/a/ad/Red_Cross_logo.svg', 'https://www.icrc.org', now()),
        (gen_random_uuid(), 'Nouvelle Vie', 'https://upload.wikimedia.org/wikipedia/en/thumb/c/c3/Nouvelle_Vie_Logo.png/220px-Nouvelle_Vie_Logo.png', 'https://nouvellevie.fr', now()),
        (gen_random_uuid(), 'WFP', 'https://upload.wikimedia.org/wikipedia/commons/4/41/WFP_Logo.svg', 'https://www.wfp.org', now());
        