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

class TestWPA2toWPA(Wifi24):

    def test_wpa2_to_wpa(self, setUp):
        """Connect WS to DUT then change sec wpa2 to wpa/wpa2
        """

        network = conn()
        assertion = Assert()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable(radio_page.get_wireless())
        radio_page.apply_changes()

        # assert wireless is enabled and wifi interface is 2.4Ghz
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        wireless = radio_page.get_wireless()
        assertion.is_true(radio_page.is_enabled(wireless), "Wireless")

        # enable primary network and wpa2 and disable wpa
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.enable(network_page.get_wpa2())
        network_page.disable(network_page.get_wpa())

        network_page.apply_changes()

        # check primary network and wpa2 are enabled and encryption is AES
        netwrk = network_page.get_primary_network()
        assertion.is_true(network_page.is_enabled(netwrk), 'Primary Network')
        wpa2 = network_page.get_wpa2()
        assertion.is_true(network_page.is_enabled(wpa2), 'WPA2 enabled')
        wpa = network_page.get_wpa()
        assertion.is_false(network_page.is_enabled(wpa), 'WPA disabled')

        # Wifi connection attempt
        network.reset_network_mngr()
        wifi_connection = network.wifi_connection(
            ssid=self.SSID, pswd=self.SSID_PASS, timeout=20)
        try:
            assertion.is_wificonnected(wifi_connection)
        except WifiConnError:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # enable wpa
        time.sleep(30)
        network_page.enable(network_page.get_wpa())

        # Set encryption to TKIP
        network_page.set_encryption("TKIP")

        network_page.apply_changes()

        # check wpa-psk is enabled and encryption is TKIP
        print(network_page.is_enabled(
                          network_page.get_wpa()))
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa()), 'WPA is enabled')
        assertion.is_equal(network_page.get_encryption(), 'TKIP+AES')

        # Disconnect wired interface
        eth_iface = network.eth_iface_name()  # get name of wired iface
        eth_disc_attempt = network.disconnect_iface(eth_iface)
        try:
            assertion.is_sucessful(eth_disc_attempt, "ethernet disconnect")
        except NetworkError:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # ping attempt
        ip = 'www.google.com'
        wifi_iface = network.wifi_iface_name()  # get name of wifi iface
        ping_attempt = network.ping_attempt(wifi_iface, ip)
        try:
            assertion.is_sucessful(ping_attempt, "ping attempt")
        finally:
            network.connect_iface(eth_iface)
            self.reset_wifisession(self.firefox, self.SSID)
