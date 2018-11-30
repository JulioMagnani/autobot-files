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

class TestValidCustomkey(Wifi5):

    def test_valid_customkey(self, setUp):
        """Check WPA2&WPA/WPA2 are working with custom key for radio 5.0Ghz"""

        # select wifi 5.0ghz and set to enabled
        self.firefox.get("http://192.168.0.1/wlanRadio.asp")
        wifi_5_iface = self.firefox.find_element_by_css_selector(
                    "select[name*='WirelessMacAddress']>option[value*='0']")
        wifi_5_iface.click()
        ssid_enable = self.firefox.find_element_by_css_selector(
                "select[name*='WirelessEnable']>option[value*='1']")
        ssid_enable.click()

        # assert ssid is enabled
        try:
            ssid_enable = WebDriverWait(self.firefox, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     "select[name*='WirelessEnable']>option[selected='']")))
        finally:
            self.assertEqual(ssid_enable.text, 'Enabled')

        # assert wifi 5.0ghz interface is selected
        self.firefox.get('http://192.168.0.1/wlanPrimaryNetwork.asp')
        wifi_5_iface = self.firefox.find_element_by_css_selector(
            "form[name*='wlanPrimaryNetwork'] > table > tbody > tr:nth-child(1) > td")
        selected_iface = wifi_5_iface.text
        self.assertEqual(selected_iface[:6], 'NET_5G')

        # enable primary network
        self.firefox.find_element_by_css_selector(
            "select[name*='PrimaryNetworkEnable']>option[value*='1']").click()

        # Select wpa-psk disable
        wpa_selector = self.firefox.find_element_by_css_selector(
                                                 "select[name*='WpaPskAuth']")
        wpa_disable_option = wpa_selector.find_element_by_css_selector(
                                                         "option[value*='0']")
        wpa_disable_option.click()

        # Select wpa2-psk enable
        wpa2_selector = self.firefox.find_element_by_css_selector(
                                                "select[name*='Wpa2PskAuth']")
        wpa2_enable_option = wpa2_selector.find_element_by_css_selector(
                                                         "option[value*='1']")
        wpa2_enable_option.click()

        # Change WiFi PASSWORD
        password = '0987654321'
        self.firefox.implicitly_wait(3)
        wifi_pswd = self.firefox.find_element_by_css_selector(
                                            "input[name*='WpaPreSharedKey']")
        wifi_pswd.clear()
        wifi_pswd.send_keys(password)  # enter password and submit.
        wifi_pswd.submit()

        # Click on Apply Button
        try:
            self.firefox.refresh()
            apply_btn = WebDriverWait(self.firefox, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[onclick*='onClickApply()']")))
        finally:
            apply_btn = self.firefox.find_element_by_css_selector(
                                         "input[onclick*='onClickApply()']")
            apply_btn.click()

        # Assert only WPA2 is enabled
        self.firefox.get('http://192.168.0.1/wlanPrimaryNetwork.asp')
        wpa_disabled = self.firefox.find_element_by_css_selector(
                              "select[name*='WpaPskAuth']>option[selected='']")
        self.assertEqual(wpa_disabled.text, 'Disabled')
        wpa2_enabled = self.firefox.find_element_by_css_selector(
                             "select[name*='Wpa2PskAuth']>option[selected='']")
        self.assertEqual(wpa2_enabled.text, 'Enabled')

        apply_btn = self.firefox.find_element_by_css_selector(
                                                "input[value*='Apply']")
        apply_btn.click()

        # Assert password was changed
        self.firefox.refresh()
        self.firefox.implicitly_wait(3)
        wifi_pswd = self.firefox.find_element_by_css_selector(
                                           "input[name*='WpaPreSharedKey']")
        current_pswd = wifi_pswd.get_attribute('value')
        self.assertEqual(current_pswd, password)

        network = conn.NetworkOps()
        # network = conn()

        # Wifi connection attempt
        wifi_connection = network.wifi_connection(
                             ssid='NET_5G215F64', pswd=password, timeout=20)
        try:
            # Check if connection attempt was successful
            self.assertTrue(wifi_connection)
            print("connection succesful")
        except AssertionError:
            print("connection failed")
            NetOps().reset_wifisession(self.firefox)
            raise

        # Disconnect the wired interface (ethernet)
        eth_iface = network.eth_iface_name()
        wired_disc_attempt = network.disconnect_iface(eth_iface)
        self.assertTrue(wired_disc_attempt)

        # Ping DUT
        wifi_iface = network.wifi_iface_name()
        DUT_ip = '192.168.0.1'
        try:
            DUT_ping_attempt = network.ping_attempt(
                                            wifi_iface, DUT_ip)
            self.assertTrue(DUT_ping_attempt)
        except AssertionError:
            print("ping failed")
            raise
        finally:
            network.connect_iface(eth_iface)
            NetOps().reset_wifisession(self.firefox)

        # Enable WPA
        self.firefox.get('http://192.168.0.1/wlanPrimaryNetwork.asp')
        wpa_enable = self.firefox.find_element_by_css_selector(
                               "select[name*='WpaPskAuth']>option[value*='1']")
        wpa_enable.click()
        tkip_enable = self.firefox.find_element_by_css_selector(
                            "select[name*='WpaEncryption']>option[value*='3']")
        tkip_enable.click()

        # Change WiFi PASSWORD
        self.firefox.implicitly_wait(3)
        wifi_pswd = self.firefox.find_element_by_css_selector(
                                            "input[name*='WpaPreSharedKey']")
        wifi_pswd.clear()
        wifi_pswd.send_keys(password)  # enter password and submit.
        wifi_pswd.submit()

        # Click on Apply Button
        try:
            self.firefox.refresh()
            apply_btn = WebDriverWait(self.firefox, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[onclick*='onClickApply()']")))
        finally:
            apply_btn = self.firefox.find_element_by_css_selector(
                                            "input[onclick*='onClickApply()']")
            apply_btn.click()

        # assert tkip is enabled
        time.sleep(2)
        assert_tkip = self.firefox.find_element_by_css_selector(
                           "select[name*='WpaEncryption']>option[selected='']")
        self.assertEqual(assert_tkip.text, 'TKIP+AES')
        print('WPA/WPA2 enabled')

        # Assert password was changed
        self.firefox.refresh()
        self.firefox.implicitly_wait(3)
        wifi_pswd = self.firefox.find_element_by_css_selector(
                                           "input[name*='WpaPreSharedKey']")
        current_pswd = wifi_pswd.get_attribute('value')
        self.assertEqual(current_pswd, password)

        # Wifi connection attempt
        wifi_connection = network.wifi_connection(
                             ssid='NET_5G215F64', pswd=password, timeout=20)
        try:
            # Check if connection attempt was successful
            self.assertTrue(wifi_connection)
            print("connection succesful")
        except AssertionError:
            print("connection failed")
            NetOps().reset_wifisession(self.firefox)
            raise

        # Disconnect the wired interface (ethernet)
        eth_iface = network.eth_iface_name()
        wired_disc_attempt = network.disconnect_iface(eth_iface)
        self.assertTrue(wired_disc_attempt)

        # Ping DUT
        wifi_iface = network.wifi_iface_name()
        DUT_ip = '192.168.0.1'
        try:
            DUT_ping_attempt = network.ping_attempt(
                                            wifi_iface, DUT_ip)
            self.assertTrue(DUT_ping_attempt)
        except AssertionError:
            print("ping failed")
            raise
        finally:
            network.connect_iface(eth_iface)
            NetOps().reset_wifisession(self.firefox)