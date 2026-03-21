# С чего начать: выкладка в App Store Connect

Пошаговый план — делайте по порядку.

---

## Шаг 0: Что нужно иметь

- [ ] **Apple ID** (обычный аккаунт Apple)
- [ ] **Оплаченный Apple Developer Program** ($99/год) — [developer.apple.com](https://developer.apple.com)
- [ ] **Xcode** установлен на Mac
- [ ] **Проект** лежит у вас на диске:  
  `Documents/pojertovania/mobailBOGDast/mobile_app`

---

## Шаг 1: Зайти в App Store Connect и создать приложение

1. Откройте **[App Store Connect](https://appstoreconnect.apple.com)** и войдите с Apple ID.
2. **Мои приложения** → кнопка **«+»** → **Новое приложение**.
3. Заполните:
   - **Платформы**: iOS  
   - **Название**: Новая Жизнь (или своё)  
   - **Основной язык**: например, Русский  
   - **Bundle ID**: создайте в Developer Portal (см. шаг 2) и выберите его здесь  
   - **SKU**: любой уникальный код, например `charity-app-001`
4. Нажмите **Создать**.

После этого приложение появится в списке в App Store Connect — это «запись» приложения, куда потом загружается билд.

---

## Шаг 2: Создать App ID (Bundle ID) в Developer Portal

1. Откройте **[Apple Developer Portal](https://developer.apple.com/account)**.
2. **Certificates, Identifiers & Profiles** → **Identifiers** → **«+»**.
3. Выберите **App IDs** → **Continue** → **App** → **Continue**.
4. Укажите:
   - **Description**: Новая Жизнь  
   - **Bundle ID**: **Explicit**, например `com.yourcompany.novayazhizn`  
   (в проекте сейчас стоит `com.charity.app.charityApp` — можно использовать его или свой).
5. **Continue** → **Register**.

Этот же Bundle ID нужно будет выбрать в App Store Connect при создании приложения (шаг 1).

---

## Шаг 3: Узнать Team ID и подставить в проект

1. В **[Apple Developer Portal](https://developer.apple.com/account)** в правом верхнем углу нажмите на своё имя/компанию.
2. В списке команд найдите **Team ID** (короткая строка букв/цифр).
3. В проекте откройте файл:  
   `mobailBOGDast/mobile_app/ios/ExportOptions.plist`  
   Найдите строку с `YOUR_TEAM_ID` и замените на ваш Team ID:
   ```xml
   <key>teamID</key>
   <string>ВАШ_TEAM_ID</string>
   ```

---

## Шаг 4: Настроить подпись в Xcode

1. Откройте проект в Xcode (из папки проекта):
   ```bash
   cd /Users/a123/Documents/pojertovania/mobailBOGDast/mobile_app/ios
   open Runner.xcworkspace
   ```
2. Слева выберите проект **Runner** (синяя иконка).
3. В центре выберите target **Runner**.
4. Вкладка **Signing & Capabilities**.
5. Включите **Automatically manage signing**.
6. В поле **Team** выберите вашу команду (должна появиться после входа в Apple ID в Xcode).

Если Team нет — в Xcode: **Xcode → Settings → Accounts** → добавьте Apple ID и выберите команду.

---

## Шаг 5: Собрать IPA

В терминале (полный путь к проекту):

```bash
cd /Users/a123/Documents/pojertovania/mobailBOGDast/mobile_app/ios
./build_for_appstore.sh 1.0.0 1
```

Если скрипт ругнётся на права:

```bash
chmod +x build_for_appstore.sh
./build_for_appstore.sh 1.0.0 1
```

После успешной сборки появится файл:  
`ios/build/ipa/Runner.ipa`

---

## Шаг 6: Загрузить билд в App Store Connect

**Вариант А — Transporter (проще):**

1. Установите приложение **Transporter** из App Store на Mac.
2. Откройте Transporter, войдите тем же Apple ID.
3. Перетащите в окно файл `Runner.ipa` из  
   `mobailBOGDast/mobile_app/ios/build/ipa/`.
4. Нажмите **Доставить**. Дождитесь окончания загрузки.

**Вариант Б — через скрипт (если настроен altool):**

```bash
cd /Users/a123/Documents/pojertovania/mobailBOGDast/mobile_app/ios
./upload_with_transporter.sh build/ipa/Runner.ipa
```

Через 5–15 минут билд появится в App Store Connect в вашем приложении (раздел версии iOS / TestFlight).

---

## Шаг 7: В App Store Connect заполнить карточку приложения

1. Снова **[App Store Connect](https://appstoreconnect.apple.com)** → ваше приложение.
2. Создайте **новую версию** (например 1.0.0) и привяжите к ней загруженный билд.
3. Заполните обязательные поля:
   - Описание приложения  
   - Ключевые слова  
   - URL поддержки  
   - Политика конфиденциальности (URL)  
   - Скриншоты (хотя бы один набор для iPhone)  
   - Иконка 1024×1024 (если ещё не задана)
4. В разделе **Сборка** выберите загруженный билд.
5. Ответьте на вопросы о рейтинге и экспорте, если спрашивает.
6. Нажмите **Отправить на проверку**.

Дальше приложение будет в статусе «На проверке». Ответ обычно приходит в течение 24–48 часов на почту Apple ID.

---

## Кратко: порядок действий

| № | Действие |
|---|----------|
| 1 | Apple Developer Program оплачен |
| 2 | App ID создан в Developer Portal |
| 3 | Приложение создано в App Store Connect |
| 4 | В проекте в `ExportOptions.plist` указан ваш Team ID |
| 5 | В Xcode включена автоматическая подпись и выбрана Team |
| 6 | Собран IPA: `./build_for_appstore.sh 1.0.0 1` |
| 7 | IPA загружен в App Store Connect (Transporter или скрипт) |
| 8 | В App Store Connect заполнены описание, скриншоты, конфиденциальность и выбран билд |
| 9 | Нажато «Отправить на проверку» |

---

## Полезные ссылки

- [App Store Connect](https://appstoreconnect.apple.com) — куда загружаете билд и заполняете карточку.
- [Apple Developer](https://developer.apple.com/account) — App ID, сертификаты, Team ID.
- Подробное руководство в проекте:  
  `mobailBOGDast/mobile_app/ios/APP_STORE_PUBLICATION_GUIDE.md`  
- Шаблон текстов для карточки:  
  `mobailBOGDast/mobile_app/ios/APP_STORE_DESCRIPTION_TEMPLATE.md`

Если что-то не получается — напишите, на каком шаге застряли (номер шага и что видите на экране).
