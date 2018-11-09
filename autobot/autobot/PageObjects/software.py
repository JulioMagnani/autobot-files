from autobot.PageObjects.pages import BasePage
from autobot.PageObjects.locators import SoftwareLocators


class SoftwarePage(BasePage):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.driver.get('http://192.168.0.1/RgSwInfo.asp')

    def get_serial_number(self):
        return self.driver.find_element(*SoftwareLocators.SERIAL_NUMBER).text
