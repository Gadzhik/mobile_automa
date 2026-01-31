from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

class BasePage:
    """
    Базовый класс для всех страниц. 
    Содержит общие методы для работы с драйвером.
    """
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)  # Явное ожидание (Explicit Wait)

    def find_element(self, locator: tuple) -> WebElement:
        """
        Находит элемент с явным ожиданием его появления.
        :param locator: Кортеж (By, value)
        :return: WebElement
        """
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator: tuple) -> None:
        """
        Кликает по элементу.
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def send_keys(self, locator: tuple, text: str) -> None:
        """
        Вводит текст в элемент.
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def tap_by_coordinates(self, x: int, y: int) -> None:
        """
        Клик по координатам (для элементов без локаторов).
        """
        # Используем W3C Actions для тапа
        self.driver.tap([(x, y)])

