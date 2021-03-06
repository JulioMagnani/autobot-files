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

class TestNModeAuto(Wifi24):

    def test_nmode_auto(self, setUp):
        """WiFi Client ping gateway's local addr with 802.11 n-mode auto"""

        assertion = Assert()
        network = conn()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable(radio_page.get_wireless())
        radio_page.enable(radio_page.get_n_mode())
        radio_page.apply_changes()

        # assert wireless is enabled and interface is 2.4Ghz
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        assertion.is_true(radio_page.is_nmode_enabled(), 'N MODE')
        wireless = radio_page.get_wireless()
        assertion.is_true(radio_page.is_enabled(wireless), "Wireless")

        # enable primary network
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())

        current_ssid_name = network_page.get_ssid_name()

        # assert primary network is enabled
        netwrk = network_page.get_primary_network()
        assertion.is_true(network_page.is_enabled(netwrk), 'Primary Network')

        # Get the DUT serial number
        soft_page = SoftwarePage(self.firefox)
        dut_serial_nb = soft_page.get_serial_number()

        # Compare digits of dut between serial number and ssid name
        ser_number_id = dut_serial_nb[-6:]  # last 6 digits of serial number
        first_half = current_ssid_name[:6]  # first 6 digits of ssid name
        last_half = current_ssid_name[-6:]  # last 6 digits of ssid name
        try:
            assertion.is_equal(first_half, "NET_2G")
            assertion.is_equal(last_half, ser_number_id)
        except WebElementError:
            # reset changes
            radio_page = RadioPage(self.firefox)
            radio_page.reset_wireless_default()
            raise

        # Wifi connection attempt
        connection_attempt = network.wifi_connection(
            ssid=self.SSID, pswd=self.SSID_PASS, timeout=20)
        try:
            assertion.is_sucessful(connection_attempt, 'connection attempt')
        except NetworkError:
            # reset changes
            radio_page = RadioPage(self.firefox)
            radio_page.reset_wireless_default()
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
        time.sleep(10)
        ping_attempt = network.ping_attempt(wifi_iface, ip)
        time.sleep(10)
        try:
            assertion.is_sucessful(ping_attempt, 'ping attempt')
        finally:
            network.connect_iface(eth_name)
            self.reset_wifisession(self.firefox, self.SSID)
