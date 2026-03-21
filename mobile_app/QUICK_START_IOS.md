# 🚀 Быстрый старт: Публикация iOS приложения в App Store

## ⚡ Быстрая инструкция

### 1️⃣ Подготовка (один раз)

1. **Зарегистрируйтесь в Apple Developer Program**
   - https://developer.apple.com ($99/год)
   - Создайте App ID в Developer Portal
   - Создайте приложение в App Store Connect

2. **Настройте Team ID**
   ```bash
   cd mobile_app/ios
   # Откройте ExportOptions.plist и замените YOUR_TEAM_ID на ваш Team ID
   ```

3. **Откройте проект в Xcode для настройки подписи**
   ```bash
   cd mobile_app/ios
   open Runner.xcworkspace
   ```
   - Выберите Runner → Signing & Capabilities
   - Включите "Automatically manage signing"
   - Выберите вашу Team

### 2️⃣ Проверка готовности

```bash
cd mobile_app/ios
./check_readiness.sh
```

### 3️⃣ Сборка приложения

```bash
cd mobile_app/ios
./build_for_appstore.sh 1.0.0 1
```

Где:
- `1.0.0` — версия приложения
- `1` — номер сборки (build number)

### 4️⃣ Загрузка в App Store Connect

**Вариант A: Через Transporter (рекомендуется)**
```bash
cd mobile_app/ios
./upload_with_transporter.sh build/ipa/Runner.ipa
```

**Вариант B: Через веб-интерфейс**
1. Откройте https://appstoreconnect.apple.com
2. Выберите ваше приложение
3. Загрузите файл `build/ipa/Runner.ipa`

### 5️⃣ Заполнение информации в App Store Connect

Следуйте инструкциям в файле:
- `ios/APP_STORE_PUBLICATION_GUIDE.md` — полное руководство
- `ios/APP_STORE_DESCRIPTION_TEMPLATE.md` — шаблон описания

### 6️⃣ Отправка на проверку

После заполнения всей информации нажмите **"Отправить на проверку"**

---

## 📚 Подробная документация

- **Полное руководство**: `ios/APP_STORE_PUBLICATION_GUIDE.md`
- **Шаблон описания**: `ios/APP_STORE_DESCRIPTION_TEMPLATE.md`

## 🆘 Помощь

Если что-то не работает:
1. Запустите `./check_readiness.sh` для диагностики
2. Проверьте раздел "Решение проблем" в полном руководстве
3. Убедитесь, что у вас есть активный Apple Developer Account

---

**Удачи! 🎉**
