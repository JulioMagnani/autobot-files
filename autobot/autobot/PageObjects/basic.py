from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from autobot.PageObjects.pages import BasePage
from autobot.PageObjects.locators import BasicLocators


class BasicPage(BasePage):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.driver.get('http://192.168.0.1/RgContentFilter.asp')

    def get_ipv6_address(self):
        ipv6_list = self.__get_ipv6()
        ipv6 = ipv6_list.text.split('/')
        ipv6_list = ''.join(ipv6[0])
        return ipv6_list

    def __get_ipv6(self):
        ipv6 = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(BasicLocators.LOCAL_IPV6))
        return ipv6
