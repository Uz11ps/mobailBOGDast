#!/bin/bash

# Скрипт для создания ключа подписи Android приложения
# Использование: ./create_keystore.sh

echo "🔐 Создание ключа для подписи Android приложения"
echo ""

# Проверяем наличие keytool
if ! command -v keytool &> /dev/null; then
    echo "❌ Ошибка: keytool не найден. Убедитесь, что установлен JDK."
    exit 1
fi

# Путь к файлу ключа
KEYSTORE_PATH="$HOME/upload-keystore.jks"

# Проверяем, существует ли уже ключ
if [ -f "$KEYSTORE_PATH" ]; then
    echo "⚠️  Внимание: Файл ключа уже существует: $KEYSTORE_PATH"
    read -p "Перезаписать? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Отменено."
        exit 0
    fi
fi

echo "Введите информацию для создания ключа:"
echo ""

# Создаем ключ
keytool -genkey -v \
    -keystore "$KEYSTORE_PATH" \
    -alias upload \
    -keyalg RSA \
    -keysize 2048 \
    -validity 10000

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Ключ успешно создан: $KEYSTORE_PATH"
    echo ""
    echo "📝 Следующие шаги:"
    echo "1. Создайте файл mobile_app/android/key.properties"
    echo "2. Добавьте в него:"
    echo "   storePassword=ВАШ_ПАРОЛЬ"
    echo "   keyPassword=ВАШ_ПАРОЛЬ"
    echo "   keyAlias=upload"
    echo "   storeFile=$KEYSTORE_PATH"
    echo ""
    echo "⚠️  ВАЖНО: Сохраните пароль и файл ключа в безопасном месте!"
else
    echo "❌ Ошибка при создании ключа"
    exit 1
fi
