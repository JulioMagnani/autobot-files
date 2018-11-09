import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from autobot.network import NetworkOps as conn
from autobot.PageObjects.basic import BasicPage
from autobot.PageObjects.login import LoginPage
from autobot.PageObjects.radio import RadioPage
from autobot.PageObjects.network import NetworkPage
from autobot.exceptions import (NetworkError, WifiConnError,
                                SeleniumServerError)
from autobot.assertion import Assert


class TestIpv6(unittest.TestCase):

    USERNAME = None
    PASSWORD = None
    SSID_24 = None
    SSID_24_PASS = None
    SSID_5 = None
    SSID_5_PASS = None

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
        cls.SSID_24 = login_info['ssid_2.4']
        cls.SSID_24_PASS = login_info['pass_2.4']
        cls.SSID_5 = login_info['ssid_5']
        cls.SSID_5_PASS = login_info['pass_5']

    @classmethod
    def reset_wifisession(cls, driver, ssid):
        conn().delete_wifi_profile(ssid=ssid)

        radio_page = RadioPage(driver)
        radio_page.reset_wireless_default()

        conn().reset_network_mngr()

    def suite(self, selected_tests):
        tests = selected_tests

        return unittest.TestSuite(map(TestIpv6, tests))

    def test_local_5_ipv6(self):
        """Check if WiFi 5GHz Client can ping gateway's local IPV6 address"""

        assertion = Assert()
        network = conn()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="5.0GHZ")
        radio_page.enable(radio_page.get_wireless())
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "5 Ghz")
        wireless = radio_page.get_wireless()
        assertion.is_true(radio_page.is_enabled(wireless), "Wireless")

        # enable primary network -> broadcast ssid
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.apply_changes()

        # assert primary network is enabled
        netwrk = network_page.get_primary_network()
        assertion.is_true(network_page.is_enabled(netwrk), 'Primary Network')

        # Get DUT local ipv6 address through WebUI
        time.sleep(2)
        basic_page = BasicPage(self.firefox)
        DUT_ipv6_addr = basic_page.get_ipv6_address()

        # Wifi connection attempt
        wifi_connection = network.wifi_connection(
            ssid=self.SSID_5, pswd=self.SSID_5_PASS, timeout=20)
        try:
            assertion.is_wificonnected(wifi_connection)
        except WifiConnError:
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

        # Ping attempt to local ipv6 of DUT
        wifi_iface = network.wifi_iface_name()
        dut_ping6_attempt = network.ping6_attempt(wifi_iface, DUT_ipv6_addr)
        try:
            assertion.is_sucessful(dut_ping6_attempt, "ping attempt")
        finally:
            network.connect_iface(eth_iface)
            self.reset_wifisession(self.firefox, self.SSID)

    def test_local_24_ipv6(self):
        """Check if WiFi 2.4GHz Client can ping gateway's local IPV6 address"""

        assertion = Assert()
        network = conn()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable(radio_page.get_wireless())
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        wireless = radio_page.get_wireless()
        assertion.is_true(radio_page.is_enabled(wireless), "Wireless")

        # enable primary network -> broadcast ssid
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.apply_changes()

        # assert primary network is enabled
        netwrk = network_page.get_primary_network()
        assertion.is_true(network_page.is_enabled(netwrk), 'Primary Network')

        # Get DUT local ipv6 address through WebUI
        time.sleep(2)
        basic_page = BasicPage(self.firefox)
        DUT_ipv6_addr = basic_page.get_ipv6_address()

        # Wifi connection attempt
        wifi_connection = network.wifi_connection(
            ssid=self.SSID_24, pswd=self.SSID_24_PASS, timeout=20)
        try:
            assertion.is_wificonnected(wifi_connection)
        except WifiConnError:
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

        # Ping attempt to local ipv6 of DUT
        wifi_iface = network.wifi_iface_name()
        dut_ping6_attempt = network.ping6_attempt(wifi_iface, DUT_ipv6_addr)
        try:
            assertion.is_sucessful(dut_ping6_attempt, "ping attempt")
        finally:
            network.connect_iface(eth_iface)
            self.reset_wifisession(self.firefox, self.SSID)
