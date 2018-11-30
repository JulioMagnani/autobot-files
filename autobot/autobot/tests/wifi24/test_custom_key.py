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

class TestCustomKey(Wifi24):

    def test_custom_key(self, setUp):
        """Set new key passphrase then connect WS to DUT.
        """

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

        # enable primary network, enable WPA2 and disable WPA
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

        # change key passphrase to '1234567890'
        password = '1234567890'
        network_page.set_password(password)
        network_page.apply_changes()

        # assert password was changed
        print(network_page.get_password())
        assertion.is_equal(network_page.get_password(), password)

        # Wifi connection attempt
        network.reset_network_mngr()
        wifi_connection = network.wifi_connection(
            ssid=self.SSID, pswd=password, timeout=20)
        try:
            assertion.is_wificonnected(wifi_connection)
        except WifiConnError:
            self.reset_wifisession(self.firefox, self.SSID)
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
        wifi_iface = network.wifi_iface_name()  # get name of wifi iface
        ip = 'www.google.com'
        time.sleep(10)
        ping_attempt = network.ping_attempt(wifi_iface, ip)
        time.sleep(10)
        try:
            assertion.is_sucessful(ping_attempt, "ping attempt")
        finally:
            network.connect_iface(eth_iface)
            self.reset_wifisession(self.firefox, self.SSID)

        # enable wpa
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_wpa())

        # Set encryption to TKIP
        network_page.set_encryption("TKIP")

        # Change WiFi password
        new_pass = 'NEW1234567890'
        network_page.set_password(new_pass)
        network_page.apply_changes()

        # check wpa-psk is enabled and encryption is TKIP
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa()), 'WPA is enabled')
        assertion.is_equal(network_page.get_encryption(), 'TKIP+AES')

        # check password is 'WpaPskChange'
        assertion.is_equal(network_page.get_password(), new_pass)

        # Wifi connection attempt
        network.reset_network_mngr()
        wifi_connection = network.wifi_connection(
            ssid=self.SSID, pswd=new_pass, timeout=20)
        try:
            assertion.is_wificonnected(wifi_connection)
        except WifiConnError:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # Disconnect wired interface
        eth_disc_attempt = network.disconnect_iface(eth_iface)
        try:
            assertion.is_sucessful(eth_disc_attempt, "ethernet disconnect")
        except NetworkError:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # ping attempt
        ip = 'www.google.com'
        ping_attempt = network.ping_attempt(wifi_iface, ip)
        try:
            assertion.is_sucessful(ping_attempt, "ping attempt")
        finally:
            network.connect_iface(eth_iface)
            self.reset_wifisession(self.firefox, self.SSID)
