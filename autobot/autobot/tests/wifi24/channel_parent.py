import time, sys, os, pytest
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

class Channel():

    @pytest.fixture()
    def setUp(self):

        self.driver = '/home/arris/Desktop/AutobotGW2/autobot/autobot/tests/wifi24/geckodriver'

        self.USERNAME = 'NET_F30882'
        self.PASSWORD = 'D42C0FF30882'
        self.SSID = 'NET_2GF30882'
        self.SSID_PASS = '0FF30882'

        self.firefox = webdriver.Firefox(executable_path=self.driver)
        login_page = LoginPage(self.firefox)
        login_page.enter_credentials(self.USERNAME, self.PASSWORD)

        yield

        self.firefox.quit() 
   
    def reset_wifisession(cls, driver, ssid):
        conn().delete_wifi_profile(ssid=ssid)

        radio_page = RadioPage(driver)
        radio_page.reset_wireless_default()

        conn().reset_network_mngr()

    def common_channel(self, band=None, channel=None, url='192.168.0.1'):
        """Base test channel test runner"""

        network = conn()
        assertion = Assert()

        # select wireless interface and bandwidth and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable(radio_page.get_wireless())
        radio_page.select_bandwidth(band)
        radio_page.set_channel(channel)
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        wireless = radio_page.get_wireless()
        assertion.is_true(radio_page.is_enabled(wireless), "Wireless")
        assertion.is_equal(radio_page.get_bandwidth(), band)
        assertion.is_equal(radio_page.get_channel(), channel)

        # enable primary network
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.apply_changes()

        # assert primary network is enabled
        netwrk = network_page.get_primary_network()
        assertion.is_true(network_page.is_enabled(netwrk), 'Primary Network')

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
        eth_iface = network.eth_iface_name()  # get name of wired iface
        eth_disc_attempt = network.disconnect_iface(eth_iface)
        try:
            assertion.is_sucessful(eth_disc_attempt, "ethernet disconnect")
        except NetworkError:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # ping attempt
        time.sleep(5)
        wifi_iface = network.wifi_iface_name()  # get name of wifi iface
        ping_attempt = network.ping_attempt(wifi_iface, url)
        time.sleep(5)
        try:
            assertion.is_sucessful(ping_attempt, "ping attempt")
        finally:
            network.connect_iface(eth_iface)
            self.reset_wifisession(self.firefox, self.SSID)