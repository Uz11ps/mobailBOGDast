# 📱 Руководство по публикации iOS приложения в App Store

Это руководство поможет вам опубликовать приложение "Новая Жизнь" в App Store.

## 📋 Предварительные требования

1. **Apple Developer Account** ($99/год)
   - Зарегистрируйтесь на https://developer.apple.com
   - Оплатите годовую подписку

2. **Xcode** (последняя версия)
   - Установите из App Store или с сайта Apple Developer

3. **Flutter SDK**
   - Убедитесь, что Flutter установлен и настроен

4. **CocoaPods**
   - Установите: `sudo gem install cocoapods`

## 🔧 Шаг 1: Настройка Apple Developer Account

### 1.1 Создание App ID

1. Войдите в [Apple Developer Portal](https://developer.apple.com/account)
2. Перейдите в **Certificates, Identifiers & Profiles**
3. Выберите **Identifiers** → **+** (создать новый)
4. Выберите **App IDs** → **Continue**
5. Выберите **App** → **Continue**
6. Заполните:
   - **Description**: Новая Жизнь
   - **Bundle ID**: `com.charity.app.charityApp` (или создайте свой уникальный)
   - Включите необходимые **Capabilities** (Push Notifications, если нужно)
7. Нажмите **Continue** → **Register**

### 1.2 Создание App Store Connect записи

1. Перейдите в [App Store Connect](https://appstoreconnect.apple.com)
2. Войдите с вашим Apple ID
3. Нажмите **Мои приложения** → **+** → **Новое приложение**
4. Заполните информацию:
   - **Платформы**: iOS
   - **Название**: Новая Жизнь
   - **Основной язык**: Русский (или другой)
   - **Bundle ID**: выберите созданный ранее App ID
   - **SKU**: уникальный идентификатор (например: `charity-app-001`)
5. Нажмите **Создать**

## 🔐 Шаг 2: Настройка сертификатов и профилей

### 2.1 Создание Distribution Certificate

**Автоматически через Xcode:**
1. Откройте проект в Xcode: `open ios/Runner.xcworkspace`
2. Выберите проект **Runner** в навигаторе
3. Выберите target **Runner**
4. Перейдите на вкладку **Signing & Capabilities**
5. Включите **Automatically manage signing**
6. Выберите вашу **Team** из выпадающего списка
7. Xcode автоматически создаст необходимые сертификаты и профили

**Вручную (если нужно):**
1. В Apple Developer Portal → **Certificates**
2. Нажмите **+** → выберите **Apple Distribution** → **Continue**
3. Следуйте инструкциям для создания CSR (Certificate Signing Request)

### 2.2 Обновление ExportOptions.plist

Откройте файл `ios/ExportOptions.plist` и замените `YOUR_TEAM_ID` на ваш Team ID:

```xml
<key>teamID</key>
<string>YOUR_TEAM_ID</string>
```

Чтобы найти Team ID:
1. Перейдите в [Apple Developer Portal](https://developer.apple.com/account)
2. В правом верхнем углу нажмите на ваше имя/компанию
3. Team ID отображается рядом с названием команды

## 🏗️ Шаг 3: Подготовка приложения

### 3.1 Обновление версии

Отредактируйте `pubspec.yaml`:

```yaml
version: 1.0.0+1  # формат: версия+build_number
```

### 3.2 Проверка настроек Info.plist

Убедитесь, что в `ios/Runner/Info.plist` указаны:
- ✅ `CFBundleDisplayName`: "Новая Жизнь"
- ✅ `CFBundleIdentifier`: соответствует App ID
- ✅ Все необходимые разрешения (камера, фото, сеть и т.д.)

### 3.3 Подготовка иконок и скриншотов

**Иконка приложения:**
- Размеры: 1024x1024 px (для App Store)
- Формат: PNG без альфа-канала
- Разместите в `ios/Runner/Assets.xcassets/AppIcon.appiconset/`

**Скриншоты для App Store:**
- iPhone 6.7": 1290 x 2796 px
- iPhone 6.5": 1242 x 2688 px
- iPhone 5.5": 1242 x 2208 px
- iPad Pro 12.9": 2048 x 2732 px

## 🔨 Шаг 4: Сборка приложения

### Вариант 1: Автоматическая сборка (рекомендуется)

```bash
cd mobile_app/ios
./build_for_appstore.sh 1.0.0 1
```

Скрипт выполнит:
- ✅ Обновление зависимостей
- ✅ Очистку предыдущих сборок
- ✅ Установку CocoaPods
- ✅ Сборку iOS приложения
- ✅ Создание архива (.xcarchive)
- ✅ Экспорт IPA файла

### Вариант 2: Ручная сборка через Xcode

1. Откройте проект:
   ```bash
   cd mobile_app/ios
   open Runner.xcworkspace
   ```

2. Выберите схему: **Runner** → **Any iOS Device**

3. В меню: **Product** → **Archive**

4. После завершения архивации откроется **Organizer**

5. Выберите архив → **Distribute App**

6. Выберите **App Store Connect** → **Next**

7. Выберите **Upload** → **Next**

8. Выберите вашу команду → **Next**

9. Проверьте настройки → **Upload**

## 📤 Шаг 5: Загрузка в App Store Connect

### Вариант 1: Через Transporter (рекомендуется)

1. Установите **Transporter** из App Store (если еще не установлен)

2. Запустите скрипт:
   ```bash
   cd mobile_app/ios
   ./upload_with_transporter.sh build/ipa/Runner.ipa
   ```

3. Или откройте Transporter вручную и перетащите IPA файл

### Вариант 2: Через веб-интерфейс

1. Перейдите в [App Store Connect](https://appstoreconnect.apple.com)
2. Выберите ваше приложение
3. Перейдите в **TestFlight** или **Версия iOS**
4. Нажмите **+ Версия** или **+ Build**
5. Загрузите IPA файл через веб-интерфейс

### Вариант 3: Через командную строку

```bash
cd mobile_app/ios
./upload_to_appstore.sh build/ipa/Runner.ipa your@email.com app-specific-password
```

**Создание App-Specific Password:**
1. Перейдите на https://appleid.apple.com
2. Войдите с вашим Apple ID
3. В разделе **Безопасность** найдите **Пароли для приложений**
4. Создайте новый пароль для "App Store Connect API"
5. Используйте этот пароль в скрипте

## 📝 Шаг 6: Заполнение информации в App Store Connect

После загрузки билда:

1. **Информация о приложении:**
   - Название (до 30 символов)
   - Подзаголовок (до 30 символов)
   - Описание (до 4000 символов)
   - Ключевые слова (до 100 символов)
   - URL поддержки
   - URL маркетинга (опционально)

2. **Цены и доступность:**
   - Выберите цену (или бесплатно)
   - Выберите страны распространения

3. **Скриншоты:**
   - Загрузите скриншоты для всех необходимых размеров устройств
   - Минимум 1 скриншот, рекомендуется 3-5

4. **Промо-текст** (опционально):
   - До 170 символов
   - Отображается над описанием

5. **Что нового в этой версии:**
   - Описание изменений (до 4000 символов)

6. **Контактная информация:**
   - Контактное лицо
   - Email для поддержки
   - Телефон (опционально)

7. **Рейтинг контента:**
   - Заполните анкету о контенте приложения

8. **Информация о конфиденциальности:**
   - URL политики конфиденциальности (обязательно)
   - Укажите, какие данные собирает приложение

## ✅ Шаг 7: Отправка на проверку

1. Убедитесь, что все поля заполнены
2. Выберите загруженный билд
3. Нажмите **Отправить на проверку**
4. Ответьте на вопросы экспорта (если применимо)
5. Подтвердите отправку

## ⏱️ Шаг 8: Ожидание проверки

- **Обычное время проверки**: 24-48 часов
- Вы получите уведомление на email о статусе проверки
- Проверяйте статус в App Store Connect

## 🔄 Обновление приложения

Для обновления:

1. Увеличьте версию в `pubspec.yaml`:
   ```yaml
   version: 1.0.1+2  # новая версия + новый build номер
   ```

2. Повторите шаги 4-7

## 🐛 Решение проблем

### Ошибка: "No signing certificate found"

**Решение:**
1. Откройте проект в Xcode
2. Выберите **Signing & Capabilities**
3. Включите **Automatically manage signing**
4. Выберите вашу Team

### Ошибка: "Invalid Bundle"

**Решение:**
- Проверьте Bundle ID в `Info.plist` и App Store Connect
- Убедитесь, что они совпадают

### Ошибка при загрузке IPA

**Решение:**
- Проверьте размер файла (должен быть < 4GB)
- Убедитесь, что используете правильный ExportOptions.plist
- Проверьте интернет-соединение

### Ошибка: "Missing Compliance"

**Решение:**
- В Info.plist добавьте:
  ```xml
  <key>ITSAppUsesNonExemptEncryption</key>
  <false/>
  ```

## 📞 Полезные ссылки

- [Apple Developer Portal](https://developer.apple.com)
- [App Store Connect](https://appstoreconnect.apple.com)
- [Flutter iOS Deployment](https://docs.flutter.dev/deployment/ios)
- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)

## 📧 Контакты поддержки

Если возникли проблемы:
- [Apple Developer Support](https://developer.apple.com/contact/)
- [Flutter Community](https://flutter.dev/community)

---

**Удачи с публикацией! 🚀**
