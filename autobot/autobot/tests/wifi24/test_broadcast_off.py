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

class TestBroadcastOff(Wifi24):

    def test_broadcast_off(self, setUp):
        """ Verify disabled SSID broadcast status"""

        assertion = Assert()
        network = conn()

        # select wireless interface and disable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.disable(radio_page.get_wireless())
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        wireless = radio_page.get_wireless()
        assertion.is_false(radio_page.is_enabled(wireless), "Wireless")

        # disable primary network
        network_page = NetworkPage(self.firefox)
        network_page.disable(network_page.get_primary_network())
        network_page.apply_changes()

        # assert primary network is enabled
        netwrk = network_page.get_primary_network()
        assertion.is_false(network_page.is_enabled(netwrk), 'Primary Network')

        # Check if ssid shows up on wifi scan
        wifi_24_ssid = network_page.get_ssid_name()
        ssid_online = network.ssid_check(ssid=wifi_24_ssid)
        try:
            assertion.is_false(ssid_online, "SSID is offline")
        finally:
            # reset changes
            radio_page = RadioPage(self.firefox)
            radio_page.reset_wireless_default()