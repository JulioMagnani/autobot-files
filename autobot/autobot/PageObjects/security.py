from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PageObjects.pages import BasePage
from PageObjects.locators import SecurityLocators


class SecurityPage(BasePage):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.driver.get('http://192.168.0.1/RgSecurity.asp')

    def factory_reset(self):
        """Perform a factory reset"""

        self.__factory_reset_yes().click()
        self.apply_changes()

    def apply_changes(self):
        self.__apply_btn().click()
        self.__alert_window()

    def __alert_window(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.alert_is_present(), 'waiting for alert message')

            alert = self.driver.switch_to.alert
            alert.accept()
            return True
        except Exception:
            return False

    def __apply_btn(self):
        return self.driver.find_element(*SecurityLocators.APPLY_BTN)

    def __factory_reset_yes(self):
        return self.driver.find_element(*SecurityLocators.RESET_FAC_YES)
