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

class TestWPA2ValidPass(Wifi24):

    def test_wpa2_validpass(self, setUp):
        """Connect to Wifi-WPA2 encryption AES with valid password"""

        network = conn()
        assertion = Assert()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable_wireless()
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        assertion.is_equal(radio_page.wireless_isenabled(), "Enabled")

        # enable wpa2
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.enable(network_page.get_wpa2())

        # Change WiFi password
        new_pass = 'Wpa2Change'
        network_page.set_password(new_pass)

        network_page.apply_changes()

        # check primary network and wpa2 are enabled and encryption is AES
        assertion.is_true(network_page.is_enabled(
                          network_page.get_primary_network()),
                          'Primary Network')
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa2()), 'WPA2 enabled')
        assertion.is_equal(network_page.get_encryption(), 'AES')

        # check password is 'Wpa2Change'
        print(network_page.get_password())
        assertion.is_equal(network_page.get_password(), new_pass)

        # Wifi connection attempt
        time.sleep(20)
        connection_attempt = network.wifi_connection(ssid=self.SSID,
                                                     pswd=new_pass)
        try:
            assertion.is_sucessful(connection_attempt, 'connection attempt')
        except NetworkError:
            self.reset_wifisession(self.firefox, self.SSID)  # reset wifi/DUT
            raise

        # Disconnect wired interface
        eth_name = network.eth_iface_name()
        eth_disc_attempt = network.disconnect_iface(eth_name)
        try:
            assertion.is_sucessful(eth_disc_attempt, 'wired disconnection')
        except NetworkError:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # Ping attempt
        wifi_iface = network.wifi_iface_name()
        ip = '192.168.0.1'
        ping_attempt = network.ping_attempt(wifi_iface, ip)
        try:
            assertion.is_sucessful(ping_attempt, 'ping attempt')
        finally:
            network.connect_iface(eth_name)
            self.reset_wifisession(self.firefox, self.SSID)
