#!/bin/bash

# Скрипт для загрузки IPA файла в App Store Connect через Transporter
# Использование: ./upload_with_transporter.sh [путь_к_ipa]
# Пример: ./upload_with_transporter.sh build/ipa/Runner.ipa

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Загрузка приложения в App Store Connect через Transporter${NC}"

# Параметры
IPA_PATH=${1:-"build/ipa/Runner.ipa"}

# Проверяем наличие IPA файла
if [ ! -f "$IPA_PATH" ]; then
    echo -e "${RED}❌ IPA файл не найден: $IPA_PATH${NC}"
    echo -e "${YELLOW}💡 Сначала запустите build_for_appstore.sh для создания IPA${NC}"
    exit 1
fi

# Проверяем наличие Transporter
if ! command -v xcrun altool &> /dev/null && ! command -v iTMSTransporter &> /dev/null; then
    echo -e "${YELLOW}⚠️  Transporter не найден. Используем альтернативный метод...${NC}"
    
    # Используем xcrun altool если доступен
    if command -v xcrun altool &> /dev/null; then
        echo -e "${GREEN}📤 Загружаем через xcrun altool...${NC}"
        echo -e "${YELLOW}💡 Вам потребуется Apple ID и App-Specific Password${NC}"
        read -p "Введите ваш Apple ID: " APPLE_ID
        read -sp "Введите App-Specific Password: " APP_SPECIFIC_PASSWORD
        echo ""
        
        xcrun altool --upload-app \
          --type ios \
          --file "$IPA_PATH" \
          --username "$APPLE_ID" \
          --password "$APP_SPECIFIC_PASSWORD"
    else
        echo -e "${RED}❌ Не удалось найти инструменты для загрузки${NC}"
        echo -e "${YELLOW}💡 Установите Xcode или Transporter из App Store${NC}"
        echo -e "${YELLOW}💡 Или используйте веб-интерфейс App Store Connect${NC}"
        exit 1
    fi
else
    # Используем Transporter (новый способ)
    echo -e "${GREEN}📤 Загружаем через Transporter...${NC}"
    
    # Находим путь к Transporter
    if [ -d "/Applications/Transporter.app" ]; then
        TRANSPORTER_PATH="/Applications/Transporter.app/Contents/itms/bin/iTMSTransporter"
    else
        TRANSPORTER_PATH=$(find /Applications -name "iTMSTransporter" 2>/dev/null | head -1)
    fi
    
    if [ -z "$TRANSPORTER_PATH" ]; then
        echo -e "${YELLOW}⚠️  Transporter не найден. Используем веб-интерфейс${NC}"
        echo -e "${GREEN}📁 IPA файл готов: $IPA_PATH${NC}"
        echo -e "${YELLOW}💡 Загрузите его вручную через App Store Connect: https://appstoreconnect.apple.com${NC}"
    else
        echo -e "${GREEN}✅ Transporter найден${NC}"
        echo -e "${YELLOW}💡 Откройте Transporter.app и загрузите файл: $IPA_PATH${NC}"
        open -a Transporter "$IPA_PATH" 2>/dev/null || echo -e "${YELLOW}⚠️  Не удалось открыть Transporter автоматически${NC}"
    fi
fi

echo -e "${GREEN}✅ Процесс загрузки завершен!${NC}"
