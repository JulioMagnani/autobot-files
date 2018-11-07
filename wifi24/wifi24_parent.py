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

    # =============================================================
    # ================  BROADCAST  ================================
    # =============================================================

    def test_bw_20(self):
        """20MHz bandwidth connectivity from a client to the DUT"""

        self.__test_bandwidth(band='20')

    def test_bw_40(self):
        """40MHz bandwidth connectivity from a client to the DUT"""

        self.__test_bandwidth(band='40')

    def __test_bandwidth(self, band=None):
        """Test Bandwidth"""

        assertion = Assert()
        network = conn()

        # select wireless interface and bandwidth and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable_wireless()
        radio_page.select_bandwidth(band)
        radio_page.apply_changes()
        radio_page.refresh_page()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        assertion.is_equal(radio_page.wireless_isenabled(), "Enabled")
        assertion.is_equal(radio_page.get_bandwidth(), band)

        # enable primary network and wpa2
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.enable(network_page.get_wpa2())

        # check primary network and wpa2 are enabled
        assertion.is_true(network_page.is_enabled(
                          network_page.get_primary_network()),
                          'Primary Network')
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa2()), 'WPA 2')

        # wifi connection attempt
        time.sleep(3)
        wifi_connection = network.wifi_connection(ssid=self.SSID,
                                                  pswd=self.SSID_PASS)
        assertion.is_wificonnected(wifi_connection)

        # Disconnect wired interface
        eth_iface = network.eth_iface_name()  # get name of wired interface
        eth_disc_attempt = network.disconnect_iface(eth_iface)
        try:
            assertion.is_sucessful(eth_disc_attempt, 'ethernet disconnect')
        except NetworkError:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # ping attempt
        wifi_iface = network.wifi_iface_name()  # get name of wifi iface
        ip = '192.168.0.1'
        ping_attempt = network.ping_attempt(wifi_iface, ip)
        try:
            assertion.is_sucessful(ping_attempt, 'ping attempt')
        finally:
            network.connect_iface(eth_iface)
            self.reset_wifisession(self.firefox, self.SSID)

    # ========================================================
    # ================  WIFI CHANNELS  =======================
    # ========================================================

    def test_internet_fix_ch(self):
        """Test internet connection w fixed channel"""

        self.__test_channel(band='20', channel='1', url='www.google.com')
	
    def test_bw20_ch1(self):
        """Test bandwidth 20/channel 1 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='1')

    def test_bw20_ch2(self):
        """Test bandwidth 20/channel 2 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='2')

    def test_bw20_ch3(self):
        """Test bandwidth 20/channel 3 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='3')

    def test_bw20_ch4(self):
        """Test bandwidth 20/channel 4 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='4')

    def test_bw20_ch5(self):
        """Test bandwidth 20/channel 5 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='5')

    def test_bw20_ch6(self):
        """Test bandwidth 20/channel 6 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='6')

    def test_bw20_ch7(self):
        """Test bandwidth 20/channel 7 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='7')

    def test_bw20_ch8(self):
        """Test bandwidth 20/channel 8 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='8')

    def test_bw20_ch9(self):
        """Test bandwidth 20/channel 9 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='9')

    def test_bw20_ch10(self):
        """Test bandwidth 20/channel 10 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='10')

    def test_bw20_ch11(self):
        """Test bandwidth 20/channel 11 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='11')

    def test_bw20_ch12(self):
        """Test bandwidth 20/channel 12 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='12')

    def test_bw20_ch13(self):
        """Test bandwidth 20/channel 13 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='13')

    def test_bw20_auto(self):
        """Test bandwidth 20/channel auto in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='0')

    def test_bw40_ch1(self):
        """Test bandwidth 40/channel 1 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='1')

    def test_bw40_ch2(self):
        """Test bandwidth 40/channel 2 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='2')

    def test_bw40_ch3(self):
        """Test bandwidth 40/channel 3 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='3')

    def test_bw40_ch4(self):
        """Test bandwidth 40/channel 4 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='4')

    def test_bw40_ch5(self):
        """Test bandwidth 40/channel 5 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='5')

    def test_bw40_ch6(self):
        """Test bandwidth 40/channel 6 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='6')

    def test_bw40_ch7(self):
        """Test bandwidth 40/channel 7 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='7')

    def test_bw40_ch8(self):
        """Test bandwidth 40/channel 8 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='8')

    def test_bw40_ch9(self):
        """Test bandwidth 40/channel 9 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='9')

    def test_bw40_auto(self):
        """Test bandwidth 40/channel auto in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='0')

    def __test_channel(self, band=None, channel=None, url='192.168.0.1'):
        """Base test channel test runner"""

        network = conn()
        assertion = Assert()

        # select wireless interface and bandwidth and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable(radio_page.get_wireless())
        radio_page.select_bandwidth(band)
        radio_page.set_channel(channel)
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        wireless = radio_page.get_wireless()
        assertion.is_true(radio_page.is_enabled(wireless), "Wireless")
        assertion.is_equal(radio_page.get_bandwidth(), band)
        assertion.is_equal(radio_page.get_channel(), channel)

        # enable primary network
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.apply_changes()

        # assert primary network is enabled
        netwrk = network_page.get_primary_network()
        assertion.is_true(network_page.is_enabled(netwrk), 'Primary Network')

        # Wifi connection attempt
        connection_attempt = network.wifi_connection(
            ssid=self.SSID, pswd=self.SSID_PASS, timeout=20)
        try:
            assertion.is_sucessful(connection_attempt, 'connection attempt')
        except NetworkError:
            # reset changes
            radio_page = RadioPage(self.firefox)
            radio_page.reset_wireless_default()
            raise

        # Disconnect wired interface
        eth_iface = network.eth_iface_name()  # get name of wired iface
        eth_disc_attempt = network.disconnect_iface(eth_iface)
        try:
            assertion.is_sucessful(eth_disc_attempt, "ethernet disconnect")
        except NetworkError:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # ping attempt
        time.sleep(5)
        wifi_iface = network.wifi_iface_name()  # get name of wifi iface
        ping_attempt = network.ping_attempt(wifi_iface, url)
        time.sleep(5)
        try:
            assertion.is_sucessful(ping_attempt, "ping attempt")
        finally:
            network.connect_iface(eth_iface)
            self.reset_wifisession(self.firefox, self.SSID)
