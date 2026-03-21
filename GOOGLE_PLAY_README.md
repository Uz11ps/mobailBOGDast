# 🚀 Публикация в Google Play - Краткая инструкция

## 📁 Файлы инструкций

1. **`GOOGLE_PLAY_PUBLICATION_GUIDE.md`** - Подробная инструкция (все шаги)
2. **`GOOGLE_PLAY_CHECKLIST.md`** - Чеклист для проверки готовности

## ⚡ Быстрый старт (3 шага)

### 1️⃣ Создайте ключ подписи

**Windows:**
```bash
create_keystore.bat
```

**Linux/Mac:**
```bash
chmod +x create_keystore.sh && ./create_keystore.sh
```

### 2️⃣ Создайте файл `mobile_app/android/key.properties`

```properties
storePassword=ВАШ_ПАРОЛЬ
keyPassword=ВАШ_ПАРОЛЬ
keyAlias=upload
storeFile=C:/Users/1/upload-keystore.jks
```

### 3️⃣ Соберите релиз

**Windows:**
```bash
build_release.bat
```

**Linux/Mac:**
```bash
chmod +x build_release.sh && ./build_release.sh
```

## 📦 Что дальше?

1. Зарегистрируйтесь в [Google Play Console](https://play.google.com/console) ($25)
2. Создайте приложение "Новая Жизнь"
3. Загрузите файл `app-release.aab` из `mobile_app/build/app/outputs/bundle/release/`
4. Заполните информацию (см. подробную инструкцию)
5. Отправьте на проверку

## 📖 Подробности

Смотрите **`GOOGLE_PLAY_PUBLICATION_GUIDE.md`** для полной инструкции.

---

**Удачи! 🎉**
