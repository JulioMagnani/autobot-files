import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from autobot.network import NetworkOps as conn
from autobot.PageObjects.security import SecurityPage
from autobot.PageObjects.login import LoginPage
from autobot.PageObjects.radio import RadioPage
from autobot.PageObjects.network import NetworkPage
from autobot.PageObjects.software import SoftwarePage
from autobot.exceptions import (NetworkError, WifiConnError, WebElementError,
                                SeleniumServerError, ElementMatchError)
from autobot.assertion import Assert


class TestWifi24(unittest.TestCase):

    USERNAME = None
    PASSWORD = None
    SSID = None
    SSID_PASS = None

    @classmethod
    def setUpClass(cls):
        try:
            cls.firefox = webdriver.Remote(
                desired_capabilities=DesiredCapabilities.FIREFOX)
        except Exception:
            raise SeleniumServerError(
                'Remote webdriver',
                'Could not reach selenium servers. Check docker!')

        login_page = LoginPage(cls.firefox)
        login_page.enter_credentials(cls.USERNAME, cls.PASSWORD)

    @classmethod
    def tearDownClass(cls):
        cls.firefox.quit()

    @classmethod
    def set_login(cls, login_info):
        cls.USERNAME = login_info['username']
        cls.PASSWORD = login_info['password']
        cls.SSID = login_info['ssid_2.4']
        cls.SSID_PASS = login_info['pass_2.4']

    @classmethod
    def reset_wifisession(cls, driver, ssid):
        conn().delete_wifi_profile(ssid=ssid)

        radio_page = RadioPage(driver)
        radio_page.reset_wireless_default()

        conn().reset_network_mngr()

    def suite(self, selected_tests):
        tests = selected_tests

        return unittest.TestSuite(map(TestWifi24, tests))

