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

class TestSSIDNewName(Wifi24):

    def test_ssid_newname(self, setUp):
        """Check DUT disconnects connected client after ssid name change
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

        # enable primary network and wpa2
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.enable(network_page.get_wpa2())

        network_page.apply_changes()

        # check primary network and wpa2 are enabled and encryption is AES
        netwrk = network_page.get_primary_network()
        assertion.is_true(network_page.is_enabled(netwrk), 'Primary Network')
        wpa2 = network_page.get_wpa2()
        assertion.is_true(network_page.is_enabled(wpa2), 'WPA2 enabled')

        # Wifi connection attempt
        network.reset_network_mngr()
        wifi_connection = network.wifi_connection(
            ssid=self.SSID, pswd=self.SSID_PASS, timeout=20)
        try:
            assertion.is_wificonnected(wifi_connection)
        except WifiConnError:
            self.reset_wifisession(self.firefox, self.SSID)
            raise
        
        # Change SSID name to 'NET_2G215F64NEWSSIDNAME'
        new_ssid = "{0}NEWSSIDNAME".format(self.SSID)
        network_page.set_ssid_name(new_ssid)
        network_page.apply_changes()

        # Assert SSID was changed
        ssid = network_page.get_ssid_name()
        try:
            assertion.is_equal(ssid, new_ssid)
        except WebElementError:
            # reset wireless configuration
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # Check if WS still connected
        time.sleep(20)
        connection_status = network.ssid_isconnected(ssid=self.SSID)
        try:
            assertion.is_false(connection_status, 'client online')
        except Exception:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # Connect to the DUT with new ssid name NET_2G215F64NEWSSIDNAME
        conn_attempt = network.wifi_connection(
            ssid=new_ssid, pswd=self.SSID_PASS)
        try:
            assertion.is_true(conn_attempt, "connection attempt")
        finally:
            network.delete_wifi_profile(ssid=new_ssid)
            self.reset_wifisession(self.firefox, self.SSID)
