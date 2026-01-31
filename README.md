# Mobile Automation Project

Этот проект содержит автотесты для мобильного приложения с использованием Python и Appium.

## Предварительные требования (Prerequisites)

Для запуска тестов необходимо убедиться, что установлены и настроены следующие компоненты:

1.  **Java Development Kit (JDK) 11+**
    *   Убедитесь, что переменная `JAVA_HOME` настроена.
    *   Проверка: `java -version`

2.  **Android SDK**
    *   Убедитесь, что переменная `ANDROID_HOME` настроена.
    *   Установите **Android SDK Platform-Tools** и **Build-Tools**.
    *   Проверка: `adb devices`

3.  **Appium Server**
    *   Установите Node.js.
    *   Установите Appium: `npm install -g appium`
    *   Установите драйвер UiAutomator2: `appium driver install uiautomator2`
    *   Проверка: `appium --version`

4.  **Android Emulator**
    *   Создайте и запустите эмулятор (в конфиге указано имя `gg1`).
    *   Проверка: `emulator -avd gg1` или через Android Studio.

## Установка зависимостей проекта

```bash
pip install -r requirements.txt
```

## Запуск тестов

1. Запустите Appium Server:
   ```bash
   appium
   ```

2. Запустите эмулятор Android.

3. Запустите тест:
   ```bash
   python test_login.py
   ```

## Структура проекта

*   `pages/` - Page Objects (описание страниц).
*   `test_login.py` - Сценарий теста.
*   `requirements.txt` - Python зависимости.
