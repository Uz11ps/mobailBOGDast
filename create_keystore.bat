@echo off
REM Скрипт для создания ключа подписи Android приложения (Windows)
REM Использование: create_keystore.bat

echo 🔐 Создание ключа для подписи Android приложения
echo.

REM Проверяем наличие keytool
where keytool >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Ошибка: keytool не найден. Убедитесь, что установлен JDK.
    pause
    exit /b 1
)

REM Путь к файлу ключа
set KEYSTORE_PATH=%USERPROFILE%\upload-keystore.jks

REM Проверяем, существует ли уже ключ
if exist "%KEYSTORE_PATH%" (
    echo ⚠️  Внимание: Файл ключа уже существует: %KEYSTORE_PATH%
    set /p OVERWRITE="Перезаписать? (y/N): "
    if /i not "%OVERWRITE%"=="y" (
        echo Отменено.
        pause
        exit /b 0
    )
)

echo Введите информацию для создания ключа:
echo.

REM Создаем ключ
keytool -genkey -v -keystore "%KEYSTORE_PATH%" -alias upload -keyalg RSA -keysize 2048 -validity 10000

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Ключ успешно создан: %KEYSTORE_PATH%
    echo.
    echo 📝 Следующие шаги:
    echo 1. Создайте файл mobile_app\android\key.properties
    echo 2. Добавьте в него:
    echo    storePassword=ВАШ_ПАРОЛЬ
    echo    keyPassword=ВАШ_ПАРОЛЬ
    echo    keyAlias=upload
    echo    storeFile=%KEYSTORE_PATH%
    echo.
    echo ⚠️  ВАЖНО: Сохраните пароль и файл ключа в безопасном месте!
) else (
    echo ❌ Ошибка при создании ключа
)

pause
