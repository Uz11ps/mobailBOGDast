#!/bin/bash

# Скрипт для сборки и архивации iOS приложения для App Store
# Использование: ./build_for_appstore.sh [версия] [build_number]
# Пример: ./build_for_appstore.sh 1.0.0 1

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Начинаем сборку iOS приложения для App Store${NC}"

# Переходим в корневую директорию проекта
cd "$(dirname "$0")/.."

# Проверяем наличие Flutter
if ! command -v flutter &> /dev/null; then
    echo -e "${RED}❌ Flutter не найден. Установите Flutter: https://flutter.dev/docs/get-started/install${NC}"
    exit 1
fi

# Проверяем наличие Xcode
if ! command -v xcodebuild &> /dev/null; then
    echo -e "${RED}❌ Xcode не найден. Установите Xcode из App Store${NC}"
    exit 1
fi

# Параметры версии
VERSION=${1:-"1.0.0"}
BUILD_NUMBER=${2:-"1"}

echo -e "${YELLOW}📦 Версия: $VERSION${NC}"
echo -e "${YELLOW}🔢 Build номер: $BUILD_NUMBER${NC}"

# Обновляем зависимости
echo -e "${GREEN}📥 Обновляем зависимости Flutter...${NC}"
flutter pub get

# Очищаем предыдущие сборки
echo -e "${GREEN}🧹 Очищаем предыдущие сборки...${NC}"
flutter clean

# Получаем зависимости снова
flutter pub get

# Переходим в iOS директорию
cd ios

# Устанавливаем Pods
echo -e "${GREEN}📦 Устанавливаем CocoaPods зависимости...${NC}"
pod install --repo-update

# Возвращаемся в корень проекта
cd ..

# Собираем iOS приложение в release режиме
echo -e "${GREEN}🔨 Собираем iOS приложение...${NC}"
flutter build ios --release --no-codesign

# Переходим в iOS директорию для архивации
cd ios

# Создаем архив
echo -e "${GREEN}📦 Создаем архив...${NC}"
xcodebuild archive \
  -workspace Runner.xcworkspace \
  -scheme Runner \
  -configuration Release \
  -archivePath build/Runner.xcarchive \
  -allowProvisioningUpdates \
  CODE_SIGN_IDENTITY="Apple Development" \
  CODE_SIGNING_REQUIRED=NO \
  CODE_SIGNING_ALLOWED=NO

echo -e "${GREEN}✅ Архив создан успешно!${NC}"
echo -e "${YELLOW}📁 Путь к архиву: $(pwd)/build/Runner.xcarchive${NC}"

# Экспортируем IPA для App Store
echo -e "${GREEN}📤 Экспортируем IPA для App Store...${NC}"

# Проверяем наличие ExportOptions.plist
if [ ! -f "ExportOptions.plist" ]; then
    echo -e "${RED}❌ Файл ExportOptions.plist не найден!${NC}"
    echo -e "${YELLOW}⚠️  Создайте ExportOptions.plist с вашим Team ID${NC}"
    exit 1
fi

xcodebuild -exportArchive \
  -archivePath build/Runner.xcarchive \
  -exportOptionsPlist ExportOptions.plist \
  -exportPath build/ipa \
  -allowProvisioningUpdates

echo -e "${GREEN}✅ IPA файл создан успешно!${NC}"
echo -e "${YELLOW}📁 Путь к IPA: $(pwd)/build/ipa/Runner.ipa${NC}"
echo -e "${GREEN}🎉 Готово! Теперь вы можете загрузить IPA в App Store Connect${NC}"
