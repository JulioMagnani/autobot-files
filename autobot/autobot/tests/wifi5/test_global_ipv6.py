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

class TestGlobalIpv6(Wifi5):

    def test_global_ipv6(self, setUp):
        """Check if a WiFi 5GHz Client can ping gateway's global IPV6 address"""

        """ Select WiFi 5GHz iface"""
        self.firefox.get("http://192.168.0.1/wlanRadio.asp")
        # select wifi 5.0ghz and set to enabled
        wifi_5_iface = self.firefox.find_element_by_css_selector(
            "select[name*='WirelessMacAddress']>option[value*='0']")
        wifi_5_iface.click()
        ssid_enable = self.firefox.find_element_by_css_selector(
            "select[name*='WirelessEnable']>option[value*='1']")
        ssid_enable.click()
        apply_btn = self.firefox.find_element_by_css_selector(
            "input[onclick*='commitRadio()']")
        apply_btn.click()

        # assert ssid is enabled
        try:
            ssid_enable = WebDriverWait(self.firefox, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                     "select[name*='WirelessEnable']>option[value*='1']")))
        finally:
            assertion.is_equal(ssid_enable.text, 'Enabled')

        # assert wifi 5.0ghz interface is selected
        self.firefox.get('http://192.168.0.1/wlanPrimaryNetwork.asp')
        wifi_5_iface = self.firefox.find_element_by_css_selector(
            "form[name*='wlanPrimaryNetwork'] > table > tbody > tr:nth-child(1) > td")
        self.assertEqual(wifi_5_iface.text, 'NET_5G215F64 (84:E0:58:21:5F:6A)')

        """Get DUT mac address through WebUI"""
        # Go to page Basic
        basic_page_link = self.firefox.find_element_by_link_text('Basic')
        basic_page_link.click()
        # get the ipv6_address
        mac_dut_el = self.firefox.find_element_by_css_selector(
            "table > tbody > tr:nth-child(6) > td:nth-child(3)")
        mac_dut = mac_dut_el.text

        """ Wifi 5GHz connection attempt"""
        # connect WS using default key passphrase
        time.sleep(3)
        network = conn.NetworkOps()
        time.sleep(65)
        try:
            connection_attempt = network.wifi_connection(
                ssid='NET_5GAE287E', timeout='50')
            self.assertTrue(connection_attempt)
            print("wifi connection established - Wifi 5.0")
        except AssertionError:
            print("Connection failed")
            NetOps().reset_wifisession(self.firefox)  # reset wifi/DUT
            raise ConnectionError

        """ Disconnect the wired interface (ethernet) """
        time.sleep(1)
        eth_iface = network.eth_iface_name()
        wired_disc_attempt = network.disconnect_iface(eth_iface)
        try:
            self.assertTrue(wired_disc_attempt)
        except AssertionError:
            NetOps().reset_wifisession(self.firefox)
            raise

        """ Get the global ipv6 of the DUT"""
        time.sleep(3)
        network = conn.NetworkOps()
        wifi_iface = network.wifi_iface_name()
        ipv6_dut = network.get_global_ipv6(wifi_iface, mac_dut)
        assert_flag = True
        print(ipv6_dut)
        if not ipv6_dut:
            assert_flag = False
        try:
            self.assertTrue(assert_flag)
        except AssertionError:
            print("Could not find the IPv6 address of DUT")
            raise

        """ Ping attempt to global ipv6 of DUT, using wifi iface"""
        try:
            dut_ping6_attempt = network.ping6_attempt(
                wifi_iface, ipv6_dut)
            self.assertTrue(dut_ping6_attempt)
        except AssertionError:
            print("Ping failed")
            raise
        finally:
            # reconfigure network interfaces to original settings
            network.connect_iface(eth_iface)
            NetOps().reset_wifisession(self.firefox)