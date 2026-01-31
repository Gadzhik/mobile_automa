import os
from dotenv import load_dotenv
import sys
import traceback
from appium import webdriver
from appium.options.android import UiAutomator2Options
from pages.login_page import LoginPage

# Добавляем корневую директорию в path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    # Настройки
    load_dotenv()
    apk_path = os.getenv('APK_PATH')

    # Настройка Desired Capabilities через Options
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'
    options.device_name = 'gg1'
    
    # Чтобы появилось окно с запросом прав, приложение должно быть переустановлено
    # или сброшено, и автоматическая выдача прав должна быть отключена.
    options.app = apk_path 
    options.no_reset = False # Сбрасывать состояние (чистый запуск)
    options.auto_grant_permissions = False # Не выдавать права автоматически
    
    # options.app_package = 'com.networkoptix.nxwitness'
    # options.app_activity = 'com.nxvms.mobile.QnActivity'

    appium_server_url = 'http://127.0.0.1:4723'

    print(f"Запуск драйвера для {apk_path}...")
    driver = None
    try:
        driver = webdriver.Remote(appium_server_url, options=options)

        # Инициализация страниц
        login_page = LoginPage(driver)

        # 1. Handle System Dialog (Allow notifications)
        login_page.allow_notification_permission()

        print("Ожидание экрана логина...")
        # 2. Login Flow
        email = os.getenv('EMAIL')
        password = os.getenv('PASSWORD')

        print(f"Попытка входа с {email}...")
        login_page.login(email, password)

        # Валидация
        print("Проверка успешности входа...")
        # Так как приложение использует SurfaceView, стандартный поиск элементов не сработает.
        # Мы делаем скриншот для визуальной проверки.
        driver.save_screenshot('final_login_result.png')
        print("SCRIPT FINISHED: Проверьте 'final_login_result.png', чтобы убедиться в успешном входе.")
        
        # Попытка проверки (скорее всего упадет или вернет False)
        if login_page.is_login_successful():
             print("SUCCESS: Элемент дашборда найден (неожиданно для SurfaceView).")
        else:
             print("INFO: Автоматическая проверка не прошла (ожидаемо для SurfaceView). См. скриншот.")

    except Exception:
        print("\n\n" + "="*50)
        print("ERROR: Произошла ошибка во время теста!")
        with open('last_error.txt', 'w') as f:
            traceback.print_exc(file=f)
        traceback.print_exc()
        print("ERROR: Check last_error.txt for details.")
        print("="*50 + "\n\n", flush=True)
        
        if driver:
             try:
                driver.save_screenshot('error_screenshot.png')
                print("Скриншот сохранен: error_screenshot.png")
                with open('page_source_dump.xml', 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                print("Page source сохранен: page_source_dump.xml")
             except:
                pass
    
    finally:
        if driver:
            print("Завершение драйвера...")
            driver.quit()

if __name__ == '__main__':
    main()
