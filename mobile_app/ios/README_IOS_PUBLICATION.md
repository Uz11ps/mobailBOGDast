# 📱 iOS Публикация в App Store - Готово к использованию!

## ✅ Что было сделано

Все необходимое для публикации вашего iOS приложения в App Store уже настроено и готово к использованию!

### 📁 Созданные файлы:

1. **`ExportOptions.plist`** — конфигурация для экспорта IPA файла
   - ⚠️ **ВАЖНО**: Замените `YOUR_TEAM_ID` на ваш реальный Team ID

2. **`build_for_appstore.sh`** — автоматическая сборка приложения
   - Обновляет зависимости
   - Собирает iOS приложение
   - Создает архив (.xcarchive)
   - Экспортирует IPA файл

3. **`upload_to_appstore.sh`** — загрузка через командную строку
   - Требует Apple ID и App-Specific Password

4. **`upload_with_transporter.sh`** — загрузка через Transporter (рекомендуется)
   - Самый простой способ загрузки

5. **`check_readiness.sh`** — проверка готовности к публикации
   - Проверяет все необходимые настройки
   - Выявляет проблемы перед сборкой

6. **`APP_STORE_PUBLICATION_GUIDE.md`** — полное руководство
   - Пошаговая инструкция
   - Решение проблем
   - Все детали процесса

7. **`APP_STORE_DESCRIPTION_TEMPLATE.md`** — шаблон описания
   - Готовые тексты для App Store Connect
   - Рекомендации по заполнению

### 🔧 Обновленные файлы:

- **`Info.plist`** — добавлены необходимые ключи для App Store:
  - `ITSAppUsesNonExemptEncryption` — для соответствия требованиям экспорта
  - Другие необходимые настройки

## 🚀 Что делать дальше

### Шаг 1: Настройка Apple Developer Account (если еще не сделано)

1. Зарегистрируйтесь: https://developer.apple.com
2. Оплатите подписку ($99/год)
3. Создайте App ID в Developer Portal
4. Создайте приложение в App Store Connect

### Шаг 2: Настройка Team ID

Откройте `ExportOptions.plist` и замените:
```xml
<key>teamID</key>
<string>YOUR_TEAM_ID</string>
```

На ваш реальный Team ID (можно найти в Apple Developer Portal).

### Шаг 3: Настройка подписи в Xcode

```bash
cd mobile_app/ios
open Runner.xcworkspace
```

В Xcode:
1. Выберите проект **Runner**
2. Выберите target **Runner**
3. Вкладка **Signing & Capabilities**
4. Включите **Automatically manage signing**
5. Выберите вашу **Team**

### Шаг 4: Проверка готовности

```bash
cd mobile_app/ios
./check_readiness.sh
```

Исправьте все найденные проблемы.

### Шаг 5: Сборка приложения

```bash
cd mobile_app/ios
./build_for_appstore.sh 1.0.0 1
```

Где:
- `1.0.0` — версия приложения (измените на нужную)
- `1` — номер сборки (увеличивайте с каждой сборкой)

### Шаг 6: Загрузка в App Store Connect

**Рекомендуемый способ:**
```bash
cd mobile_app/ios
./upload_with_transporter.sh build/ipa/Runner.ipa
```

Или загрузите `build/ipa/Runner.ipa` через веб-интерфейс App Store Connect.

### Шаг 7: Заполнение информации в App Store Connect

Используйте шаблон из `APP_STORE_DESCRIPTION_TEMPLATE.md` для заполнения:
- Название приложения
- Описание
- Скриншоты
- Информация о конфиденциальности
- И т.д.

### Шаг 8: Отправка на проверку

После заполнения всей информации нажмите **"Отправить на проверку"** в App Store Connect.

## 📚 Документация

- **Быстрый старт**: `../QUICK_START_IOS.md`
- **Полное руководство**: `APP_STORE_PUBLICATION_GUIDE.md`
- **Шаблон описания**: `APP_STORE_DESCRIPTION_TEMPLATE.md`

## ⚠️ Важные замечания

1. **Team ID** — обязательно замените в `ExportOptions.plist`
2. **Версия** — обновляйте версию в `pubspec.yaml` перед каждой сборкой
3. **Build Number** — должен увеличиваться с каждой сборкой
4. **Иконка** — убедитесь, что есть иконка 1024x1024 для App Store
5. **Скриншоты** — подготовьте скриншоты для разных размеров устройств

## 🆘 Помощь

Если возникли проблемы:

1. Запустите `./check_readiness.sh` для диагностики
2. Проверьте раздел "Решение проблем" в `APP_STORE_PUBLICATION_GUIDE.md`
3. Убедитесь, что:
   - У вас активный Apple Developer Account
   - Xcode установлен и настроен
   - Flutter установлен и настроен
   - CocoaPods установлен

## 📞 Полезные ссылки

- [Apple Developer Portal](https://developer.apple.com)
- [App Store Connect](https://appstoreconnect.apple.com)
- [Flutter iOS Deployment](https://docs.flutter.dev/deployment/ios)
- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)

---

**Все готово! Удачи с публикацией! 🎉**
