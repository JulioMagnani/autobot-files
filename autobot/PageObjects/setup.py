from autobot.PageObjects.pages import BasePage


class SetupPage(BasePage):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.driver.get('http://192.168.0.1/RgSetup.asp')
