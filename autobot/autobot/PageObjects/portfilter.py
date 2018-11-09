from autobot.PageObjects.pages import BasePage


class PortFilterPage(BasePage):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.driver.get('http://192.168.0.1/RgPortFiltering.asp')
