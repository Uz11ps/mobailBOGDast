#!/bin/bash

# Скрипт для загрузки IPA файла в App Store Connect
# Использование: ./upload_to_appstore.sh [путь_к_ipa] [apple_id] [app_specific_password]
# Пример: ./upload_to_appstore.sh build/ipa/Runner.ipa your@email.com xxxx-xxxx-xxxx-xxxx

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Загрузка приложения в App Store Connect${NC}"

# Параметры
IPA_PATH=${1:-"build/ipa/Runner.ipa"}
APPLE_ID=${2}
APP_SPECIFIC_PASSWORD=${3}

# Проверяем наличие IPA файла
if [ ! -f "$IPA_PATH" ]; then
    echo -e "${RED}❌ IPA файл не найден: $IPA_PATH${NC}"
    echo -e "${YELLOW}💡 Сначала запустите build_for_appstore.sh для создания IPA${NC}"
    exit 1
fi

# Проверяем наличие Apple ID
if [ -z "$APPLE_ID" ]; then
    echo -e "${YELLOW}⚠️  Apple ID не указан${NC}"
    read -p "Введите ваш Apple ID: " APPLE_ID
fi

# Проверяем наличие App-Specific Password
if [ -z "$APP_SPECIFIC_PASSWORD" ]; then
    echo -e "${YELLOW}⚠️  App-Specific Password не указан${NC}"
    echo -e "${YELLOW}💡 Создайте App-Specific Password на https://appleid.apple.com${NC}"
    read -sp "Введите App-Specific Password: " APP_SPECIFIC_PASSWORD
    echo ""
fi

# Проверяем наличие altool или xcrun altool
if command -v xcrun altool &> /dev/null; then
    UPLOAD_TOOL="xcrun altool"
elif command -v altool &> /dev/null; then
    UPLOAD_TOOL="altool"
else
    echo -e "${RED}❌ altool не найден. Установите Xcode Command Line Tools${NC}"
    exit 1
fi

echo -e "${GREEN}📤 Загружаем IPA в App Store Connect...${NC}"

# Загружаем через altool (старый способ)
$UPLOAD_TOOL --upload-app \
  --type ios \
  --file "$IPA_PATH" \
  --username "$APPLE_ID" \
  --password "$APP_SPECIFIC_PASSWORD"

echo -e "${GREEN}✅ Приложение успешно загружено в App Store Connect!${NC}"
echo -e "${YELLOW}💡 Теперь перейдите в App Store Connect для завершения публикации${NC}"
