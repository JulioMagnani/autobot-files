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

class TestWrongpass(Wifi5):

    def test_wpa2_wrongpass(self, setUp):
        """Connect WS to DUT with incorrect passkey in WPA2 mode"""

        # select wifi 5.0ghz and set to enabled
        self.firefox.get("http://192.168.0.1/wlanRadio.asp")
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
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "select[name*='WirelessEnable']>option[selected='']")))
        finally:
            self.assertEqual(ssid_enable.text, 'Enabled')

        # assert wifi 5.0ghz interface is selected
        self.firefox.get('http://192.168.0.1/wlanPrimaryNetwork.asp')
        wifi_5_iface = self.firefox.find_element_by_css_selector(
            "form[name*='wlanPrimaryNetwork'] > table > tbody > tr:nth-child(1) > td")
        selected_iface = wifi_5_iface.text
        self.assertEqual(selected_iface[:6], 'NET_5G')

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
        password = 'Wpa2Pass'
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
                    (By.CSS_SELECTOR,
                     "input[onclick*='onClickApply()']")))
        finally:

            apply_btn = self.firefox.find_element_by_css_selector(
                                     "input[onclick*='onClickApply()']")
            apply_btn.click()

        # Assert the password was changed
        self.firefox.implicitly_wait(3)
        wifi_pswd = self.firefox.find_element_by_css_selector(
                                      "input[name*='WpaPreSharedKey']")
        current_pswd = wifi_pswd.get_attribute('value')
        self.assertEqual(current_pswd, password)

        """ Wifi connection attempt"""
        # network = conn.NetworkOps()
        network = conn.NetworkOps()
        time.sleep(65)
        inc_pswd = 'WPA2PASS'  # incorrect password

        try:
            # asserts if the WiFi connection was not successful
            wifi_connection = network.wifi_connection(ssid='NET_5G215F64',
                                                      pswd=inc_pswd,
                                                      timeout='20')
            self.assertFalse(wifi_connection)
            print("connection failed")
        except AssertionError:
            print("connection succeeded. Test failed")
            raise
        finally:
            NetOps().reset_wifisession(self.firefox)
            time.sleep(10)