@echo off
REM Скрипт для сборки релизной версии приложения для Google Play
REM Использование: build_release.bat

echo 🚀 Сборка релизной версии приложения для Google Play
echo.

REM Переходим в директорию mobile_app
cd /d "%~dp0mobile_app"

REM Проверяем наличие key.properties
if not exist "android\key.properties" (
    echo ❌ Ошибка: Файл android\key.properties не найден!
    echo.
    echo Создайте файл android\key.properties на основе android\key.properties.example
    echo и заполните его реальными значениями.
    pause
    exit /b 1
)

echo 📦 Сборка App Bundle (рекомендуется Google Play)...
flutter build appbundle --release

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ App Bundle успешно создан!
    echo 📁 Файл: build\app\outputs\bundle\release\app-release.aab
    echo.
    echo 📦 Альтернатива - сборка APK...
    flutter build apk --release
    echo.
    echo ✅ APK успешно создан!
    echo 📁 Файл: build\app\outputs\flutter-apk\app-release.apk
    echo.
    echo 🎉 Готово! Теперь загрузите файл в Google Play Console.
) else (
    echo ❌ Ошибка при сборке
    pause
    exit /b 1
)

pause
