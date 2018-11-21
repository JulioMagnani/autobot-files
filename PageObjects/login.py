from PageObjects.pages import BasePage
from PageObjects.locators import LoginLocators


class LoginPage(BasePage):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.driver.get('http://192.168.0.1/')

    def enter_credentials(self, username, password):
        USERNAME = self.driver.find_element(*LoginLocators.USERNAME)
        PASSWORD = self.driver.find_element(*LoginLocators.PASSWORD)
        APPLY_BTN = self.driver.find_element(*LoginLocators.APPLY_BTN)

        USERNAME.send_keys(username)
        PASSWORD.send_keys(password)
        APPLY_BTN.click()
