from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from autobot.PageObjects.pages import BasePage
from autobot.PageObjects.locators import MacFilterLocators


class MacFilterPage(BasePage):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.driver.get('http://192.168.0.1/RgMacFiltering.asp')

    def set_mac_address(self, adrr):
        """Set mac address in Web UI Advanced Page"""
        MAC_ADDRESS = self.__mac_addr()

        MAC_ADDRESS.clear()
        MAC_ADDRESS.send_keys(adrr)

    def check_error_page(self):
        return self.__error_window()

    def click_add_btn(self):
        self.__add_mac_btn().click()
        self.refresh_page()

    def click_clear_all_btn(self):
        self.__clear_all_btn().click()
        self.refresh_page()

    def __mac_addr(self):
        return self.driver.find_element(*MacFilterLocators.MAC_ADDRESS)

    def __add_mac_btn(self):
        return self.driver.find_element(*MacFilterLocators.ADD_MAC_BTN)

    def __clear_all_btn(self):
        return self.driver.find_element(*MacFilterLocators.RM_ALL_BTN)

    def __error_link(self):
        return self.driver.find_element(*MacFilterLocators.ERROR_LINK)

    def __error_window(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.alert_is_present(), 'waiting for alert message')

            alert = self.driver.switch_to.alert
            alert.accept()
            return True
        except Exception:
            return False
