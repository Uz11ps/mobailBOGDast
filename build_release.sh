#!/bin/bash

# Скрипт для сборки релизной версии приложения для Google Play
# Использование: ./build_release.sh

echo "🚀 Сборка релизной версии приложения для Google Play"
echo ""

# Переходим в директорию mobile_app
cd "$(dirname "$0")/mobile_app" || exit 1

# Проверяем наличие key.properties
if [ ! -f "android/key.properties" ]; then
    echo "❌ Ошибка: Файл android/key.properties не найден!"
    echo ""
    echo "Создайте файл android/key.properties на основе android/key.properties.example"
    echo "и заполните его реальными значениями."
    exit 1
fi

echo "📦 Сборка App Bundle (рекомендуется Google Play)..."
flutter build appbundle --release

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ App Bundle успешно создан!"
    echo "📁 Файл: build/app/outputs/bundle/release/app-release.aab"
    echo ""
    echo "📦 Альтернатива - сборка APK..."
    flutter build apk --release
    echo ""
    echo "✅ APK успешно создан!"
    echo "📁 Файл: build/app/outputs/flutter-apk/app-release.apk"
    echo ""
    echo "🎉 Готово! Теперь загрузите файл в Google Play Console."
else
    echo "❌ Ошибка при сборке"
    exit 1
fi
