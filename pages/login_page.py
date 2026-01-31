from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class LoginPage(BasePage):
    """
    Страница авторизации.
    Содержит локаторы и методы для взаимодействия с элементами входа.
    """

    # Локаторы (примерные, так как реальные ID зависят от приложения)
    # Используем accessibility_id или xpath/id в зависимости от того, что доступно
    _EMAIL_INPUT = (AppiumBy.XPATH, "//android.widget.EditText[contains(@resource-id, 'email') or contains(@text, 'Email')]")
    _PASSWORD_INPUT = (AppiumBy.XPATH, "//android.widget.EditText[contains(@resource-id, 'password') or contains(@text, 'Password')]")
    # Кнопка может быть 'Login', 'Log in', 'Submit' и т.д.
    _LOGIN_BUTTON = (AppiumBy.XPATH, "//android.widget.Button[contains(@text, 'Login') or contains(@text, 'Submit') or contains(@content-desc, 'Login')]")
    
    # Локатор элемента, который подтверждает успешный вход (например, элемент дашборда)
    _DASHBOARD_ELEMENT = (AppiumBy.XPATH, "//*[contains(@resource-id, 'dashboard') or contains(@text, 'Dashboard')]")

    def enter_email(self, email: str) -> None:
        """Вводит email."""
        self.send_keys(self._EMAIL_INPUT, email)

    def enter_password(self, password: str) -> None:
        """Вводит пароль."""
        self.send_keys(self._PASSWORD_INPUT, password)

    def click_login(self) -> None:
        """Нажимает кнопку логина."""
        self.click(self._LOGIN_BUTTON)

    # Локаторы
    _ALLOW_NOTIFICATIONS_BUTTON = (AppiumBy.XPATH, "//android.widget.Button[@text='Allow']")
    
    # Локаторы формы входа (предполагаем, что оверлей нативный)
    # Email field
    _EMAIL_INPUT = (AppiumBy.XPATH, "//android.widget.EditText[contains(@text, 'Email') or contains(@resource-id, 'email') or @class='android.widget.EditText']")
    _NEXT_BUTTON = (AppiumBy.XPATH, "//android.widget.Button[contains(@text, 'Next') or contains(@content-desc, 'Next')]")
    
    # Password field
    _PASSWORD_INPUT = (AppiumBy.XPATH, "//android.widget.EditText[contains(@text, 'Password') or contains(@resource-id, 'password')]")
    _LOGIN_BUTTON = (AppiumBy.XPATH, "//android.widget.Button[contains(@text, 'Log In') or contains(@text, 'Login')]")

    def allow_notification_permission(self) -> None:
        """1. Initial Permission"""
        try:
            print("Checking for notification permission dialog...")
            short_wait = WebDriverWait(self.driver, 5) 
            element = short_wait.until(EC.presence_of_element_located(self._ALLOW_NOTIFICATIONS_BUTTON))
            element.click()
            print("Notification permission allowed")
        except:
            print("Notification permission dialog did not appear (or already allowed).")
        
        print("Initial Wait: Waiting 5 seconds for app to load...")
        import time
        time.sleep(5)

    def open_login_menu(self) -> None:
        """2. Open Login Menu (Screenshot 2)"""
        print("Step: Open Menu")
        # Top-left corner (Nx Logo). Coords: 100, 150
        print("Action: Click Top-Left Menu (100, 150)")
        self.tap_by_coordinates(100, 150)
        
        print("Wait: 3 seconds for transition...")
        import time
        time.sleep(3)

    def type_text_via_adb(self, text: str) -> None:
        """
        Ввод текста через ADB (самый надежный способ для 'слепых' полей).
        """
        import subprocess
        try:
            subprocess.run(f"adb shell input text '{text}'", shell=True, check=True)
        except Exception as e:
            print(f"Failed to type via ADB: {e}")

    def enter_email_step(self, email: str) -> None:
        """3. Enter Email (Screenshot 3)"""
        print("Step: Enter Email")
        import time
        import subprocess

        # Email Field Location: ~Center-Top. Coords: 540, 900
        print("Action: Click Email Input (540, 900)")
        self.tap_by_coordinates(540, 900)
        time.sleep(2) # Focus wait
        
        print(f"Action: Type Email '{email}' via ADB")
        self.type_text_via_adb(email)
        
        # Confirm Entry: Enter (66)
        print("Action: Press ENTER (keyevent 66)")
        subprocess.run("adb shell input keyevent 66", shell=True)
        time.sleep(1)

        # Hide Keyboard: Back (4)
        print("Action: Hide Keyboard (keyevent 4)")
        subprocess.run("adb shell input keyevent 4", shell=True)
        
        # Wait for UI to react
        print("Wait: 2 seconds for UI reaction...")
        time.sleep(2)
             
        # Next Button Location: Below Email. Coords: 540, 1100
        print("Action: Click Next Button (540, 1100)")
        self.tap_by_coordinates(540, 1100)
        
        print("Wait: 3 seconds for Password field transition...")
        time.sleep(3)

    def enter_password_step(self, password: str) -> None:
        """4. Enter Password (Screenshot 4)"""
        print("Step: Enter Password")
        import time
        import subprocess

        # Password Field Location. Coords: 540, 1000
        print("Action: Click Password Input (540, 1000)")
        self.tap_by_coordinates(540, 1000)
        time.sleep(2)
        
        print("Action: Type Password via ADB")
        self.type_text_via_adb(password)

        # Confirm Entry: Enter (66) - Vital for App detection
        print("Action: Press ENTER (keyevent 66)")
        subprocess.run("adb shell input keyevent 66", shell=True)
        time.sleep(1)

        # Hide Keyboard: Back (4) - Reveal UI
        print("Action: Hide Keyboard (keyevent 4)")
        subprocess.run("adb shell input keyevent 4", shell=True)
        
        print("Wait: 2 seconds for UI reaction...")
        time.sleep(2)
        
        # Log In Button Location. Coords: 540, 1200
        print("Action: Click Log In Button (540, 1200)")
        # Strategy: Double Tap / Persistent Click
        self.tap_by_coordinates(540, 1200)
        time.sleep(0.5)
        print("Action: Double Tap confirmation...")
        self.tap_by_coordinates(540, 1200)
        
        print("Wait: 5 seconds for Login to complete...")
        time.sleep(5)
        
    def login(self, email: str, passw: str) -> None:
        # Full Sequence
        self.open_login_menu()
        self.enter_email_step(email)
        self.enter_password_step(passw)

    def is_login_successful(self) -> bool:
        """
        Проверяет успешность входа по наличию элемента дашборда.
        """
        try:
            self.wait.until(EC.presence_of_element_located(self._DASHBOARD_ELEMENT))
            return True
        except:
            return False
