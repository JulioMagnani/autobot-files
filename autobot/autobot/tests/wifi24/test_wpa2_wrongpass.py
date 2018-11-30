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

class TestWPA2WrongPass(Wifi24):

    def test_wpa2_wrongpass(self, setUp):
        """Attempt to connect to Wifi-WPA2 encryption AES with wrong password
        """

        network = conn()
        assertion = Assert()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable(radio_page.get_wireless())
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        wireless = radio_page.get_wireless()
        assertion.is_true(radio_page.is_enabled(wireless), "Wireless")

        # enable both wpa2 and wpa
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

        # check password is 'WpaPskChange'
        assertion.is_equal(network_page.get_password(), new_pass)

        # Wifi connection attempt
        time.sleep(20)
        connection_attempt = network.wifi_connection(ssid=self.SSID,
                                                     pswd='WrongPass')
        try:
            assertion.is_unsucessful(connection_attempt, 'connection attempt')
        finally:
            self.reset_wifisession(self.firefox, self.SSID)
