import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from autobot.network import NetworkOps as conn
from autobot.PageObjects.basic import BasicPage
from autobot.PageObjects.security import SecurityPage
from autobot.PageObjects.login import LoginPage
from autobot.PageObjects.radio import RadioPage
from autobot.PageObjects.network import NetworkPage
from autobot.PageObjects.software import SoftwarePage

from autobot.exceptions import (NetworkError, WifiConnError, WebElementError,
                                SeleniumServerError)
from autobot.assertion import Assert


class TestWifi5(unittest.TestCase):

    USERNAME = None
    PASSWORD = None
    SSID = None
    SSID_PASS = None

    @classmethod
    def setUpClass(cls):
        cls.firefox = webdriver.Remote(
            desired_capabilities=DesiredCapabilities.FIREFOX)

        cls.firefox.get('http://192.168.0.1')
        cls.firefox.find_element_by_name('loginUsername').send_keys(
                                                       cls.USERNAME)
        cls.firefox.find_element_by_name('loginPassword').send_keys(
                                                       cls.PASSWORD)
        cls.firefox.find_element_by_css_selector(
              'tbody>tr:nth-child(3)>td>input[type=submit]').click()

    @classmethod
    def tearDownClass(cls):
        cls.firefox.quit()

    def suite(self, selected_tests):
        tests = selected_tests

        return unittest.TestSuite(map(TestWifi5, tests))

    @classmethod
    def set_login(cls, login_info):
        cls.USERNAME = login_info['username']
        cls.PASSWORD = login_info['password']
        cls.SSID = login_info['ssid_5']
        cls.SSID_PASS = login_info['pass_5']

    @classmethod
    def reset_wifisession(cls, driver, ssid):
        conn().delete_wifi_profile(ssid=ssid)

        driver.get('http://192.168.0.1/wlanRadio.asp')
        driver.find_element_by_css_selector(
            "input[value*='Restore Wireless Defaults']").click()
        conn().reset_network_mngr()