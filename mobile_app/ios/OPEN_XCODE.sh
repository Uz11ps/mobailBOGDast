#!/bin/bash

# Скрипт для открытия проекта в Xcode
# Использование: ./OPEN_XCODE.sh

cd "$(dirname "$0")"
echo "📂 Текущая директория: $(pwd)"
echo "🚀 Открываю Runner.xcworkspace в Xcode..."

if [ -d "Runner.xcworkspace" ]; then
    open Runner.xcworkspace
    echo "✅ Проект открыт в Xcode!"
else
    echo "❌ Ошибка: Runner.xcworkspace не найден"
    echo "💡 Убедитесь, что вы находитесь в правильной директории"
    exit 1
fi
