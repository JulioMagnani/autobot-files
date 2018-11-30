import time, sys, os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from wifi24 import Wifi24

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "{}/{}".format(os.path.pardir,os.path.pardir))))

from assertion import Assert
from network import NetworkOps as conn
from PageObjects.security import SecurityPage
from PageObjects.login import LoginPage
from PageObjects.radio import RadioPage
from PageObjects.network import NetworkPage
from PageObjects.software import SoftwarePage
from exceptions import (NetworkError, WifiConnError, WebElementError,SeleniumServerError, ElementMatchError)

class TestDenyOpensec(Wifi24):

    def test_deny_opensec(self, setUp):
        """DUT denies access to client without password"""

        network = conn()
        assertion = Assert()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable_wireless()
        radio_page.apply_changes()

        # assert wireless is enabled and bandwidth is 2.4Ghz
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        assertion.is_equal(radio_page.wireless_isenabled(), "Enabled")

        # enable Primary Network and WPA2 and disable WPA
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.enable(network_page.get_wpa2())
        network_page.disable(network_page.get_wpa())
        network_page.apply_changes()

        # Assert only WPA2 is enabled
        assertion.is_true(network_page.is_enabled(
                          network_page.get_primary_network()),
                          'Primary Network')
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa2()), 'WPA 2')
        assertion.is_false(network_page.is_enabled(
                          network_page.get_wpa()), 'WPA')

        # Wifi connection attempt
        network.reset_network_mngr()
        wifi_connection = network.wifi_connection_nosec(ssid=self.SSID)
        try:
            assertion.is_false(wifi_connection, 'wifi connection')
        finally:
            self.reset_wifisession(self.firefox, self.SSID)

        # enable wpa and set encryption to TKIP
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_wpa())
        network_page.set_encryption("TKIP")
        network_page.apply_changes()

        # check wpa-psk is enabled and encryption is TKIP
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa()), 'WPA is enabled')
        assertion.is_equal(network_page.get_encryption(), 'TKIP+AES')

        # Wifi connection attempt
        network.reset_network_mngr()
        wifi_connection = network.wifi_connection_nosec(ssid=self.SSID)
        try:
            assertion.is_false(wifi_connection, 'wifi connection')
        finally:
            self.reset_wifisession(self.firefox, self.SSID)

        # disable WPA2
        network_page = NetworkPage(self.firefox)
        network_page.disable(network_page.get_wpa2())
        network_page.apply_changes()

        # assert WPA2 (therefore WPA too for 3P Box) is disabled
        assertion.is_false(network_page.is_enabled(
                           network_page.get_wpa2()), 'WPA 2')

        # Wifi connection attempt
        network.reset_network_mngr()
        time.sleep(5)
        wifi_connection = network.wifi_connection_nosec(ssid=self.SSID)
        try:
            assertion.is_wificonnected(wifi_connection)
        finally:
            self.reset_wifisession(self.firefox, self.SSID)
