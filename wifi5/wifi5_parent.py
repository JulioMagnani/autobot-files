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

    # =======================================================
    # ================  WIFI CHANNELS  ======================
    # =======================================================
    def test_bw20_ch0(self):
        """Connect client to bandwidth 20/channel auto 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='0')

    def test_bw20_ch36(self):
        """Connect client to bandwidth 20/channel 36 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='36')

    def test_bw20_ch40(self):
        """Connect client to bandwidth 20/channel 40 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='40')

    def test_bw20_ch44(self):
        """Connect client to bandwidth 20/channel 44 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='44')

    def test_bw20_ch48(self):
        """Connect client to bandwidth 20/channel 48 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='48')

    def test_bw20_ch52(self):
        """Connect client to bandwidth 20/channel 52 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='52')

    def test_bw20_ch56(self):
        """Connect client to bandwidth 20/channel 56 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='56')

    def test_bw20_ch60(self):
        """Connect client to bandwidth 20/channel 60 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='60')

    def test_bw20_ch64(self):
        """Connect client to bandwidth 20/channel 64 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='64')

    def test_bw20_ch100(self):
        """Connect client to bandwidth 20/channel 100 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='100')

    def test_bw20_ch104(self):
        """Connect client to bandwidth 20/channel 104 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='104')

    def test_bw20_ch108(self):
        """Connect client to bandwidth 20/channel 108 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='108')

    def test_bw20_ch112(self):
        """Connect client to bandwidth 20/channel 112 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='112')

    def test_bw20_ch116(self):
        """Connect client to bandwidth 20/channel 116 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='116')

    def test_bw20_ch120(self):
        """Connect client to bandwidth 20/channel 120 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='120')

    def test_bw20_ch124(self):
        """Connect client to bandwidth 20/channel 124 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='124')

    def test_bw20_ch128(self):
        """Connect client to bandwidth 20/channel 128 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='128')

    def test_bw20_ch132(self):
        """Connect client to bandwidth 20/channel 132 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='132')

    def test_bw20_ch136(self):
        """Connect client to bandwidth 20/channel 136 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='136')

    def test_bw20_ch140(self):
        """Connect client to bandwidth 20/channel 140 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='140')

    def test_bw20_ch144(self):
        """Connect client to bandwidth 20/channel 144 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='144')

    def test_bw20_ch149(self):
        """Connect client to bandwidth 20/channel 149 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='149')

    def test_bw20_ch153(self):
        """Connect client to bandwidth 20/channel 153 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='153')

    def test_bw20_ch157(self):
        """Connect client to bandwidth 20/channel 157 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='157')

    def test_bw20_ch161(self):
        """Connect client to bandwidth 20/channel 161 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='161')

    def test_bw20_ch165(self):
        """Connect client to bandwidth 20/channel 165 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='165')

    def test_bw40_ch0(self):
        """Connect client to bandwidth 40/channel auto 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='0')

    def test_bw40_ch36(self):
        """Connect client to bandwidth 40/channel 36 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='36')

    def test_bw40_ch44(self):
        """Connect client to bandwidth 40/channel 44 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='44')

    def test_bw40_ch52(self):
        """Connect client to bandwidth 40/channel 52 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='52')

    def test_bw40_ch60(self):
        """Connect client to bandwidth 40/channel 60 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='60')

    def test_bw40_ch100(self):
        """Connect client to bandwidth 40/channel 100 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='100')

    def test_bw40_ch108(self):
        """Connect client to bandwidth 40/channel 108 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='108')

    def test_bw40_ch116(self):
        """Connect client to bandwidth 40/channel 116 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='116')

    def test_bw40_ch124(self):
        """Connect client to bandwidth 40/channel 124 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='124')

    def test_bw40_ch132(self):
        """Connect client to bandwidth 40/channel 132 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='132')

    def test_bw40_ch140(self):
        """Connect client to bandwidth 40/channel 140 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='140')

    def test_bw40_ch149(self):
        """Connect client to bandwidth 40/channel 149 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='149')

    def test_bw40_ch157(self):
        """Connect client to bandwidth 40/channel 157 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='157')

    def test_bw80_ch0(self):
        """Connect client to bandwidth 80/channel auto 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='0/80')

    def test_bw80_ch36(self):
        """Connect client to bandwidth 80/channel 36 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='36/80')

    def test_bw80_ch40(self):
        """Connect client to bandwidth 80/channel 40 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='40/80')

    def test_bw80_ch44(self):
        """Connect client to bandwidth 80/channel 44 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='44/80')

    def test_bw80_ch48(self):
        """Connect client to bandwidth 80/channel 48 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='48/80')

    def test_bw80_ch52(self):
        """Connect client to bandwidth 80/channel 52 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='52/80')

    def test_bw80_ch56(self):
        """Connect client to bandwidth 80/channel 56 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='56/80')

    def test_bw80_ch60(self):
        """Connect client to bandwidth 80/channel 60 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='60/80')

    def test_bw80_ch64(self):
        """Connect client to bandwidth 80/channel 64 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='64/80')

    def test_bw80_ch100(self):
        """Connect client to bandwidth 80/channel 100 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='100/80')

    def test_bw80_ch104(self):
        """Connect client to bandwidth 80/channel 104 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='104/80')

    def test_bw80_ch108(self):
        """Connect client to bandwidth 80/channel 108 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='108/80')

    def test_bw80_ch112(self):
        """Connect client to bandwidth 80/channel 112 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='112/80')

    def test_bw80_ch116(self):
        """Connect client to bandwidth 80/channel 116 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='116/80')

    def test_bw80_ch120(self):
        """Connect client to bandwidth 80/channel 120 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='120/80')

    def test_bw80_ch124(self):
        """Connect client to bandwidth 80/channel 124 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='124/80')

    def test_bw80_ch128(self):
        """Connect client to bandwidth 80/channel 128 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='128/80')

    def test_bw80_ch132(self):
        """Connect client to bandwidth 80/channel 132 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='132/80')

    def test_bw80_ch136(self):
        """Connect client to bandwidth 80/channel 136 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='136/80')

    def test_bw80_ch140(self):
        """Connect client to bandwidth 80/channel 140 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='140/80')

    def test_bw80_ch144(self):
        """Connect client to bandwidth 80/channel 144 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='144/80')

    def test_bw80_ch149(self):
        """Connect client to bandwidth 80/channel 149 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='149/80')

    def test_bw80_ch153(self):
        """Connect client to bandwidth 80/channel 153 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='153/80')

    def test_bw80_ch157(self):
        """Connect client to bandwidth 80/channel 157 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='157/80')

    def test_bw80_ch161(self):
        """Connect client to bandwidth 80/channel 161 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='161/80')
