from autobot.PageObjects.pages import BasePage


class DmzPage(BasePage):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.driver.get('http://192.168.0.1/RgDmzHost.asp')
