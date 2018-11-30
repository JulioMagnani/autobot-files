import time, sys, os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wifi5 import Wifi5

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "{}/{}".format(os.path.pardir,os.path.pardir))))

from network import NetworkOps as conn
from PageObjects.basic import BasicPage
from PageObjects.security import SecurityPage
from PageObjects.login import LoginPage
from PageObjects.radio import RadioPage
from PageObjects.network import NetworkPage
from PageObjects.software import SoftwarePage

from exceptions import (NetworkError, WifiConnError, WebElementError,
                                SeleniumServerError)
from assertion import Assert

class TestSSIDBroadcast(Wifi5):

    def test_ssidbroadcast(self, setUp):
        """Check 5.0Ghz ssid visibility from client and beacon broadcast
        """

        assertion = Assert()
        network = conn()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="5.0GHZ")
        radio_page.enable(radio_page.get_wireless())
        radio_page.set_channel('36')
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

        # Check if ssid shows up on wifi scan
        time.sleep(65)
        wifi_24_ssid = network_page.get_ssid_name()
        print(network_page.get_ssid_name())
        ssid_online = network.ssid_check(ssid=wifi_24_ssid)
        try:
            assertion.is_true(ssid_online, "SSID is online")
        except WebElementError:
            # reset changes
            radio_page = RadioPage(self.firefox)
            radio_page.reset_wireless_default()
            raise

        # activate monitor mode

        # analyze tshark wireless iface: filter by channel and SSID
        # is_online = network.find_ssid_bychannel(channel=36, ssid=self.SSID)
        # try:
        #     assertion.is_true(is_online, "SSID is online - tshark")
        # finally:
            # reset changes
        #     radio_page = RadioPage(self.firefox)
        #     radio_page.reset_wireless_default()
        #     raise