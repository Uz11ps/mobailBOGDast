#!/bin/bash

# Скрипт для проверки готовности приложения к публикации в App Store
# Использование: ./check_readiness.sh

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Проверка готовности приложения к публикации в App Store${NC}\n"

ERRORS=0
WARNINGS=0

# Функция для проверки
check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
        ((ERRORS++))
    fi
}

warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    ((WARNINGS++))
}

# Переходим в корневую директорию проекта
cd "$(dirname "$0")/.."

echo -e "${BLUE}📱 Проверка Flutter окружения...${NC}"
command -v flutter &> /dev/null && check "Flutter установлен" || warn "Flutter не найден"

if command -v flutter &> /dev/null; then
    flutter doctor | grep -q "Xcode" && check "Xcode настроен" || warn "Xcode не настроен"
    flutter doctor | grep -q "CocoaPods" && check "CocoaPods настроен" || warn "CocoaPods не настроен"
fi

echo -e "\n${BLUE}📦 Проверка файлов проекта...${NC}"

[ -f "pubspec.yaml" ] && check "pubspec.yaml существует" || warn "pubspec.yaml не найден"
[ -f "ios/Runner/Info.plist" ] && check "Info.plist существует" || warn "Info.plist не найден"
[ -f "ios/Podfile" ] && check "Podfile существует" || warn "Podfile не найден"
[ -f "ios/ExportOptions.plist" ] && check "ExportOptions.plist существует" || warn "ExportOptions.plist не найден"

echo -e "\n${BLUE}🔐 Проверка настроек подписи...${NC}"

if [ -f "ios/Runner/Info.plist" ]; then
    grep -q "CFBundleDisplayName" ios/Runner/Info.plist && check "CFBundleDisplayName установлен" || warn "CFBundleDisplayName не установлен"
    grep -q "ITSAppUsesNonExemptEncryption" ios/Runner/Info.plist && check "ITSAppUsesNonExemptEncryption установлен" || warn "ITSAppUsesNonExemptEncryption не установлен"
fi

if [ -f "ios/ExportOptions.plist" ]; then
    if grep -q "YOUR_TEAM_ID" ios/ExportOptions.plist; then
        warn "Team ID не настроен в ExportOptions.plist"
    else
        check "Team ID настроен в ExportOptions.plist"
    fi
fi

echo -e "\n${BLUE}📝 Проверка версии...${NC}"

if [ -f "pubspec.yaml" ]; then
    VERSION=$(grep "^version:" pubspec.yaml | sed 's/version: //' | tr -d ' ')
    if [ -n "$VERSION" ]; then
        check "Версия установлена: $VERSION"
    else
        warn "Версия не установлена в pubspec.yaml"
    fi
fi

echo -e "\n${BLUE}🖼️  Проверка ресурсов...${NC}"

if [ -d "ios/Runner/Assets.xcassets/AppIcon.appiconset" ]; then
    ICON_COUNT=$(find ios/Runner/Assets.xcassets/AppIcon.appiconset -name "*.png" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$ICON_COUNT" -gt 0 ]; then
        check "Иконки приложения найдены ($ICON_COUNT файлов)"
    else
        warn "Иконки приложения не найдены"
    fi
else
    warn "Папка с иконками не найдена"
fi

echo -e "\n${BLUE}🔨 Проверка скриптов...${NC}"

[ -x "ios/build_for_appstore.sh" ] && check "build_for_appstore.sh исполняемый" || warn "build_for_appstore.sh не исполняемый"
[ -x "ios/upload_to_appstore.sh" ] && check "upload_to_appstore.sh исполняемый" || warn "upload_to_appstore.sh не исполняемый"
[ -x "ios/upload_with_transporter.sh" ] && check "upload_with_transporter.sh исполняемый" || warn "upload_with_transporter.sh не исполняемый"

echo -e "\n${BLUE}📋 Итоги проверки:${NC}"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}🎉 Все проверки пройдены! Приложение готово к публикации.${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Найдено предупреждений: $WARNINGS${NC}"
    echo -e "${YELLOW}💡 Рекомендуется исправить предупреждения перед публикацией${NC}"
    exit 0
else
    echo -e "${RED}❌ Найдено ошибок: $ERRORS${NC}"
    echo -e "${RED}⚠️  Найдено предупреждений: $WARNINGS${NC}"
    echo -e "${RED}💡 Исправьте ошибки перед публикацией${NC}"
    exit 1
fi
