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

class TestWPSIsEnabled(Wifi24):

    def test_wps_isenabled(self, setUp):
        """Check WPS is enabled by default on wifi 2.4Ghz
        """

        assertion = Assert()

        # factory reset
        security_page = SecurityPage(self.firefox)
        security_page.factory_reset()
        time.sleep(60)

        # log in
        login_page = LoginPage(self.firefox)
        login_page.enter_credentials(self.USERNAME, self.PASSWORD)

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable(radio_page.get_wireless())
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        wireless = radio_page.get_wireless()
        assertion.is_true(radio_page.is_enabled(wireless), "Wireless")

        # enable primary network
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.apply_changes()

        # assert primary network and wps are enabled
        netwrk = network_page.get_primary_network()
        assertion.is_true(network_page.is_enabled(netwrk), 'Primary Network')
        wps = network_page.get_wps()
        time.sleep(10)
        assertion.is_true(network_page.is_wps_enabled(wps), 'WPS')

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="5.0GHZ")
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "5 Ghz")

        # assert wps is enabled
        network_page = NetworkPage(self.firefox)
        wps = network_page.get_wps()
        assertion.is_true(network_page.is_wps_enabled(wps), 'WPS')