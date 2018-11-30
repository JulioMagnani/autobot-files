import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from autobot.network import NetworkOps as conn
from autobot.PageObjects.basic import BasicPage
from autobot.PageObjects.security import SecurityPage
from autobot.PageObjects.login import LoginPage
from autobot.PageObjects.radio import RadioPage
from autobot.PageObjects.network import NetworkPage
from autobot.PageObjects.software import SoftwarePage

from autobot.exceptions import (NetworkError, WifiConnError, WebElementError,
                                SeleniumServerError)
from autobot.assertion import Assert


class TestWifi5(unittest.TestCase):

    USERNAME = None
    PASSWORD = None
    SSID = None
    SSID_PASS = None

    @classmethod
    def setUpClass(cls):
        cls.firefox = webdriver.Remote(
            desired_capabilities=DesiredCapabilities.FIREFOX)

        cls.firefox.get('http://192.168.0.1')
        cls.firefox.find_element_by_name('loginUsername').send_keys(
                                                       cls.USERNAME)
        cls.firefox.find_element_by_name('loginPassword').send_keys(
                                                       cls.PASSWORD)
        cls.firefox.find_element_by_css_selector(
              'tbody>tr:nth-child(3)>td>input[type=submit]').click()

    @classmethod
    def tearDownClass(cls):
        cls.firefox.quit()

    def suite(self, selected_tests):
        tests = selected_tests

        return unittest.TestSuite(map(TestWifi5, tests))

    @classmethod
    def set_login(cls, login_info):
        cls.USERNAME = login_info['username']
        cls.PASSWORD = login_info['password']
        cls.SSID = login_info['ssid_5']
        cls.SSID_PASS = login_info['pass_5']

    @classmethod
    def reset_wifisession(cls, driver, ssid):
        conn().delete_wifi_profile(ssid=ssid)

        driver.get('http://192.168.0.1/wlanRadio.asp')
        driver.find_element_by_css_selector(
            "input[value*='Restore Wireless Defaults']").click()
        conn().reset_network_mngr()

    def test_defaultkey(self):
        """Connect client to DUT wifi 5.0Ghz network with default key
        """

        assertion = Assert()
        network = conn()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="5.0GHZ")
        radio_page.enable(radio_page.get_wireless())
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

        # Wifi connection attempt
        wifi_connection = network.wifi_connection(
            ssid=self.SSID, pswd=self.SSID_PASS, timeout=20)
        try:
            assertion.is_wificonnected(wifi_connection)
        except WifiConnError:
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
        ip = '192.168.0.1'
        wifi_iface = network.wifi_iface_name()  # get name of wifi iface
        ping_attempt = network.ping_attempt(wifi_iface, ip)
        try:
            assertion.is_sucessful(ping_attempt, "ping attempt")
        finally:
            network.connect_iface(eth_iface)
            self.reset_wifisession(self.firefox, self.SSID)

    def test_ssidbroadcast(self):
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

    def test_local_ipv6(self):
        """Check if a WiFi 5GHz Client can ping gateway's local IPV6 address"""

        assertion = Assert()
        network = conn()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="5.0GHZ")
        radio_page.enable(radio_page.get_wireless())
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

        # Get DUT local ipv6 address through WebUI
        time.sleep(2)
        basic_page = BasicPage(self.firefox)
        DUT_ipv6_addr = basic_page.get_ipv6_address()

        # Wifi connection attempt
        wifi_connection = network.wifi_connection(
            ssid=self.SSID, pswd=self.SSID_PASS, timeout=20)
        try:
            assertion.is_wificonnected(wifi_connection)
        except WifiConnError:
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

        # Ping attempt to local ipv6 of DUT
        wifi_iface = network.wifi_iface_name()
        dut_ping6_attempt = network.ping6_attempt(wifi_iface, DUT_ipv6_addr)
        try:
            assertion.is_sucessful(dut_ping6_attempt, "ping attempt")
        finally:
            network.connect_iface(eth_iface)
            self.reset_wifisession(self.firefox, self.SSID)

    def test_global_ipv6(self):
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
            self.assertEqual(ssid_enable.text, 'Enabled')

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

    def test_deny_client(self):
        """Check if DUT denies client connection attempt

        Try to connect to WPA2 and WPA/WPA2 security without providing
        passkey.
        """
        self.firefox.get("http://192.168.0.1/wlanRadio.asp")

        """ select wifi 5.0ghz and set to enabled """
        wifi_5_iface = self.firefox.find_element_by_css_selector(
                    "select[name*='WirelessMacAddress']>option[value*='0']")
        wifi_5_iface.click()
        ssid_enable = self.firefox.find_element_by_css_selector(
                "select[name*='WirelessEnable']>option[value*='1']")
        ssid_enable.click()
        apply_btn = self.firefox.find_element_by_css_selector(
                                             "input[onclick*='commitRadio()']")
        apply_btn.click()

        """ assert ssid is enabled """
        try:
            ssid_enable = WebDriverWait(self.firefox, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "select[name*='WirelessEnable']>option[selected='']")))
        finally:
            self.assertEqual(ssid_enable.text, 'Enabled')

        """ assert wifi 5.0ghz interface is selected """
        self.firefox.get('http://192.168.0.1/wlanPrimaryNetwork.asp')
        wifi_5_iface = self.firefox.find_element_by_css_selector(
            "form[name*='wlanPrimaryNetwork'] > table > tbody > tr:nth-child(1) > td")
        selected_iface = wifi_5_iface.text
        self.assertEqual(selected_iface[:6], 'NET_5G')

        """ Disable WPA and set network security to WPA2 """
        self.firefox.get('http://192.168.0.1/wlanPrimaryNetwork.asp')

        wpa_disable = self.firefox.find_element_by_css_selector(
                               "select[name*='WpaPskAuth']>option[value*='0']")
        wpa_disable.click()
        wpa2_enable = self.firefox.find_element_by_css_selector(
                              "select[name*='Wpa2PskAuth']>option[value*='1']")
        wpa2_enable.click()
        apply_btn = self.firefox.find_element_by_css_selector(
                                            "input[onclick*='onClickApply()']")
        apply_btn.click()

        """ Assert only WPA2 is enabled """
        wpa_disabled = self.firefox.find_element_by_css_selector(
                              "select[name*='WpaPskAuth']>option[selected='']")
        self.assertEqual(wpa_disabled.text, 'Disabled')
        wpa2_enabled = self.firefox.find_element_by_css_selector(
                             "select[name*='Wpa2PskAuth']>option[selected='']")
        self.assertEqual(wpa2_enabled.text, 'Enabled')

        """ Try to connect client with no sec to WPA2 network """
        network = conn.NetworkOps()
        try:
            conn_attempt = network.wifi_connection_nosec(ssid='NET_5GAE287E', timeout=20)
            self.assertFalse(conn_attempt)
            """ connection attempt to WPA2 failed """
        except AssertionError:
            print("Connection was successful")
            raise ConnectionError
        finally:
            network.delete_wifi_profile(ssid='NET_5GAE287E')

        """ enable WPA and TKIP encryption """
        wpa_enable = self.firefox.find_element_by_css_selector(
                               "select[name*='WpaPskAuth']>option[value*='1']")
        wpa_enable.click()
        tkip_enable = self.firefox.find_element_by_css_selector(
                            "select[name*='WpaEncryption']>option[value*='3']")
        tkip_enable.click()
        apply_btn = self.firefox.find_element_by_css_selector(
                                            "input[onclick*='onClickApply()']")
        apply_btn.click()

        """ assert tkip is enabled - only possible if wpa is enabled """
        assert_tkip = self.firefox.find_element_by_css_selector(
                           "select[name*='WpaEncryption']>option[selected='']")
        self.assertEqual(assert_tkip.text, 'TKIP+AES')

        """ Try to connect client with no sec to WPA2 network """
        try:
            conn_attempt = network.wifi_connection_nosec(ssid='NET_5G215F64', timeout=20)
            self.assertFalse(conn_attempt)
            print("connection attempt to WPA/WPA2 - TKIP failed")
        except AssertionError:
            print("Connection was successful")
            raise AssertionError
        finally:
            NetOps().reset_wifisession(self.firefox)

    def test_open_security(self):
        """Connect client to open wifi network"""

        """ select wifi 5.0ghz and set to enabled """
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

        """ assert ssid is enabled """
        try:
            ssid_enable = WebDriverWait(self.firefox, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "select[name*='WirelessEnable']>option[selected='']")))
        finally:
            self.assertEqual(ssid_enable.text, 'Enabled')

        """ assert wifi 5.0ghz interface is selected """
        self.firefox.get('http://192.168.0.1/wlanPrimaryNetwork.asp')
        wifi_5_iface = self.firefox.find_element_by_css_selector(
            "form[name*='wlanPrimaryNetwork'] > table > tbody > tr:nth-child(1) > td")
        selected_iface = wifi_5_iface.text
        self.assertEqual(selected_iface[:6], 'NET_5G')

        """ Disable security """
        self.firefox.get('http://192.168.0.1/wlanPrimaryNetwork.asp')
        wpa2_selector = self.firefox.find_element_by_css_selector(
                        "select[name*='Wpa2PskAuth']>option[value*='0']")
        wpa2_selector.click()
        apply_btn = self.firefox.find_element_by_css_selector(
                                                 "input[value*='Apply']")
        apply_btn.click()

        """ handle popup // click ok button """
        self.firefox.switch_to.alert.accept()

        """ Check encryption is disabled """
        time.sleep(5)
        ck_wap2_disabled = self.firefox.find_element_by_css_selector(
            "select[name*='Wpa2PskAuth']>option[selected='']")
        encryp_menu = self.firefox.find_element_by_name('WpaEncryption')
        try:
            self.assertEqual(ck_wap2_disabled.text, 'Disabled')
            self.assertEqual(encryp_menu.text, 'Disabled')
        except AssertionError:
            print("encryption is not set to open")
            raise AssertionError

        """ Wifi connection attempt """
        time.sleep(65)
        network = conn.NetworkOps()
        network.reset_network_mngr()
        try:
            connection_attempt = network.wifi_connection_nosec(
                                     ssid='NET_5G215F64', timeout='90')
            self.assertTrue(connection_attempt)
            print("wifi connection established")
        except AssertionError:
            print("Connection failed")
            NetOps().reset_wifisession(self.firefox)
            raise

        """ Disconnect wired interface(ethernet) """
        eth_name = network.eth_iface_name()
        disc_wiredconn = network.disconnect_iface(eth_name)
        self.assertTrue(disc_wiredconn)

        """ Ping attempt """
        print('Ping google.com')
        wifi_iface = network.wifi_iface_name()
        try:
            ping_attempt = network.ping_attempt(wifi_iface, 'www.google.com')
            self.assertTrue(ping_attempt)
        except AssertionError:
            print("ping failed")
            raise
        finally:
            """ reconnect ethernet and delete wifi profile """
            network.connect_iface(eth_name)
            NetOps().reset_wifisession(self.firefox)
            time.sleep(60)

    def test_wpa2_wrongpass(self):
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

    def test_wpa2_validpass(self):
        """Connect WS to DUT with valid passkey in WPA2 mode"""

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
                    (By.CSS_SELECTOR, "input[onclick*='onClickApply()']")))
        finally:
            apply_btn = self.firefox.find_element_by_css_selector(
                                         "input[onclick*='onClickApply()']")
            apply_btn.click()

        # Assert if the password was changed
        self.firefox.refresh()
        self.firefox.implicitly_wait(3)
        wifi_pswd = self.firefox.find_element_by_css_selector(
                                           "input[name*='WpaPreSharedKey']")
        current_pswd = wifi_pswd.get_attribute('value')
        print(current_pswd)
        self.assertEqual(current_pswd, password)

        """ Wifi connection attempt"""
        # network = conn.NetworkOps()
        network = conn.NetworkOps()
        time.sleep(65)
        network.reset_network_mngr()
        time.sleep(1)
        try:
            wifi_connection = network.wifi_connection(ssid='NET_5G215F64',
                                                      pswd=current_pswd,
                                                      timeout='90')
            self.assertTrue(wifi_connection)
        except AssertionError:
            print('connection failed')
            network.reset_network_mngr()
            raise

        """ Disconnect the wired interface (ethernet) """
        eth_iface = network.eth_iface_name()
        wired_disc_attempt = network.disconnect_iface(eth_iface)
        self.assertTrue(wired_disc_attempt)

        """ Check the Internet connectivity from the wlan client"""
        # Ping attempt to arris oficial website
        time.sleep(5)
        # get the name of the wifi iface
        wifi_iface = network.wifi_iface_name()
        internet_ip = 'www.google.com'
        try:
            internet_ping_attempt = network.ping_attempt(
                                            wifi_iface, internet_ip)
            self.assertTrue(internet_ping_attempt)
        except AssertionError:
            print("ping failed")
            raise
        finally:
            network.connect_iface(eth_iface)
            NetOps().reset_wifisession(self.firefox)
            time.sleep(10)

    def test_valid_customkey(self):
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

    def test_internet_auto_ch(self):
        """ Test Internet conn. from a wlan host using auto ch. mode"""

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
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     "select[name*='WirelessEnable']>option[value*='1']")))
        finally:
            self.assertEqual(ssid_enable.text, 'Enabled')
        # assert wifi 5.0ghz interface is selected
        self.firefox.get('http://192.168.0.1/wlanPrimaryNetwork.asp')
        wifi_5_iface = self.firefox.find_element_by_css_selector(
            "form[name*='wlanPrimaryNetwork'] > table > tbody > tr:nth-child(1) > td")
        self.assertEqual(wifi_5_iface.text, 'NET_5G215F64 (84:E0:58:21:5F:6A)')

        """ Select auto channel broadcasting mode """
        # Open Wireless page
        self.wireless_page_link = self.firefox.find_element_by_link_text(
            'Wireless')
        self.wireless_page_link.click()
        # Change selector to 5Ghz interface
        iface_selector = self.firefox.find_element_by_name(
            "WirelessMacAddress")
        iface_selector.find_element_by_css_selector(
            "option[value*='0']").click()
        # Select auto channel for broadcasting
        channel_el = self.firefox.find_element_by_name(
            "ChannelNumber")
        channel_el.find_element_by_css_selector(
            "option[value*='0']").click()
        # Click on Apply Button
        apply_btn = self.firefox.find_element_by_css_selector(
            "input[onclick*='commitRadio()']")
        apply_btn.click()
        time.sleep(10)
        self.firefox.refresh()
        time.sleep(2)

        """ Assert if current channel is auto """
        # Change selector to 2.4Ghz interface
        iface_selector = self.firefox.find_element_by_name(
            "WirelessMacAddress")
        iface_selector.find_element_by_css_selector(
            "option[value*='0']").click()
        current_ch_el = self.firefox.find_element_by_name(
            "ChannelNumber")
        current_ch = current_ch_el.find_element_by_css_selector(
            "option[selected]").text
        try:
            self.assertEqual(current_ch, 'Auto')
        except AssertionError:
            print("Channel could not be set to auto mode.")
            raise

        """ Wifi 5GHz connection attempt"""
        # Connect WS using default key passphrase
        time.sleep(3)
        network = conn.NetworkOps()
        time.sleep(65)
        try:
            connection_attempt = network.wifi_connection(
                ssid='NET_5G215F64', timeout='90')
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

        """ Internet ping attempt"""
        time.sleep(5)
        # get the name of the wifi iface
        wifi_iface = network.wifi_iface_name()
        internet_website = 'www.google.com'
        try:
            internet_ping_attempt = network.ping_attempt_100(
                wifi_iface, internet_website)
            self.assertTrue(internet_ping_attempt)
        except AssertionError:
            print("Ping failed")
            raise
        finally:
            # reconfigure network interfaces to original settings
            network.connect_iface(eth_iface)
            NetOps().reset_wifisession(self.firefox)

    # =======================================================
    # ================  WIFI CHANNELS  ======================
    # =======================================================
    def test_bw20_ch0(self):
        """Connect client to bandwidth 20/channel auto 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='0')

    def test_bw20_ch36(self):
        """Connect client to bandwidth 20/channel 36 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='36')

    def test_bw20_ch40(self):
        """Connect client to bandwidth 20/channel 40 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='40')

    def test_bw20_ch44(self):
        """Connect client to bandwidth 20/channel 44 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='44')

    def test_bw20_ch48(self):
        """Connect client to bandwidth 20/channel 48 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='48')

    def test_bw20_ch52(self):
        """Connect client to bandwidth 20/channel 52 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='52')

    def test_bw20_ch56(self):
        """Connect client to bandwidth 20/channel 56 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='56')

    def test_bw20_ch60(self):
        """Connect client to bandwidth 20/channel 60 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='60')

    def test_bw20_ch64(self):
        """Connect client to bandwidth 20/channel 64 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='64')

    def test_bw20_ch100(self):
        """Connect client to bandwidth 20/channel 100 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='100')

    def test_bw20_ch104(self):
        """Connect client to bandwidth 20/channel 104 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='104')

    def test_bw20_ch108(self):
        """Connect client to bandwidth 20/channel 108 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='108')

    def test_bw20_ch112(self):
        """Connect client to bandwidth 20/channel 112 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='112')

    def test_bw20_ch116(self):
        """Connect client to bandwidth 20/channel 116 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='116')

    def test_bw20_ch120(self):
        """Connect client to bandwidth 20/channel 120 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='120')

    def test_bw20_ch124(self):
        """Connect client to bandwidth 20/channel 124 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='124')

    def test_bw20_ch128(self):
        """Connect client to bandwidth 20/channel 128 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='128')

    def test_bw20_ch132(self):
        """Connect client to bandwidth 20/channel 132 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='132')

    def test_bw20_ch136(self):
        """Connect client to bandwidth 20/channel 136 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='136')

    def test_bw20_ch140(self):
        """Connect client to bandwidth 20/channel 140 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='140')

    def test_bw20_ch144(self):
        """Connect client to bandwidth 20/channel 144 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='144')

    def test_bw20_ch149(self):
        """Connect client to bandwidth 20/channel 149 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='149')

    def test_bw20_ch153(self):
        """Connect client to bandwidth 20/channel 153 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='153')

    def test_bw20_ch157(self):
        """Connect client to bandwidth 20/channel 157 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='157')

    def test_bw20_ch161(self):
        """Connect client to bandwidth 20/channel 161 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='161')

    def test_bw20_ch165(self):
        """Connect client to bandwidth 20/channel 165 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='165')

    def test_bw40_ch0(self):
        """Connect client to bandwidth 40/channel auto 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='0')

    def test_bw40_ch36(self):
        """Connect client to bandwidth 40/channel 36 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='36')

    def test_bw40_ch44(self):
        """Connect client to bandwidth 40/channel 44 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='44')

    def test_bw40_ch52(self):
        """Connect client to bandwidth 40/channel 52 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='52')

    def test_bw40_ch60(self):
        """Connect client to bandwidth 40/channel 60 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='60')

    def test_bw40_ch100(self):
        """Connect client to bandwidth 40/channel 100 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='100')

    def test_bw40_ch108(self):
        """Connect client to bandwidth 40/channel 108 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='108')

    def test_bw40_ch116(self):
        """Connect client to bandwidth 40/channel 116 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='116')

    def test_bw40_ch124(self):
        """Connect client to bandwidth 40/channel 124 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='124')

    def test_bw40_ch132(self):
        """Connect client to bandwidth 40/channel 132 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='132')

    def test_bw40_ch140(self):
        """Connect client to bandwidth 40/channel 140 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='140')

    def test_bw40_ch149(self):
        """Connect client to bandwidth 40/channel 149 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='149')

    def test_bw40_ch157(self):
        """Connect client to bandwidth 40/channel 157 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='157')

    def test_bw80_ch0(self):
        """Connect client to bandwidth 80/channel auto 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='0/80')

    def test_bw80_ch36(self):
        """Connect client to bandwidth 80/channel 36 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='36/80')

    def test_bw80_ch40(self):
        """Connect client to bandwidth 80/channel 40 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='40/80')

    def test_bw80_ch44(self):
        """Connect client to bandwidth 80/channel 44 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='44/80')

    def test_bw80_ch48(self):
        """Connect client to bandwidth 80/channel 48 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='48/80')

    def test_bw80_ch52(self):
        """Connect client to bandwidth 80/channel 52 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='52/80')

    def test_bw80_ch56(self):
        """Connect client to bandwidth 80/channel 56 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='56/80')

    def test_bw80_ch60(self):
        """Connect client to bandwidth 80/channel 60 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='60/80')

    def test_bw80_ch64(self):
        """Connect client to bandwidth 80/channel 64 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='64/80')

    def test_bw80_ch100(self):
        """Connect client to bandwidth 80/channel 100 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='100/80')

    def test_bw80_ch104(self):
        """Connect client to bandwidth 80/channel 104 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='104/80')

    def test_bw80_ch108(self):
        """Connect client to bandwidth 80/channel 108 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='108/80')

    def test_bw80_ch112(self):
        """Connect client to bandwidth 80/channel 112 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='112/80')

    def test_bw80_ch116(self):
        """Connect client to bandwidth 80/channel 116 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='116/80')

    def test_bw80_ch120(self):
        """Connect client to bandwidth 80/channel 120 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='120/80')

    def test_bw80_ch124(self):
        """Connect client to bandwidth 80/channel 124 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='124/80')

    def test_bw80_ch128(self):
        """Connect client to bandwidth 80/channel 128 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='128/80')

    def test_bw80_ch132(self):
        """Connect client to bandwidth 80/channel 132 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='132/80')

    def test_bw80_ch136(self):
        """Connect client to bandwidth 80/channel 136 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='136/80')

    def test_bw80_ch140(self):
        """Connect client to bandwidth 80/channel 140 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='140/80')

    def test_bw80_ch144(self):
        """Connect client to bandwidth 80/channel 144 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='144/80')

    def test_bw80_ch149(self):
        """Connect client to bandwidth 80/channel 149 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='149/80')

    def test_bw80_ch153(self):
        """Connect client to bandwidth 80/channel 153 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='153/80')

    def test_bw80_ch157(self):
        """Connect client to bandwidth 80/channel 157 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='157/80')

    def test_bw80_ch161(self):
        """Connect client to bandwidth 80/channel 161 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='161/80')

    def __test_channel(self, band=None, channel=None):
        """Connect client to band and channel provided"""

        network = conn()
        assertion = Assert()

        # select wireless interface and bandwidth and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="5.0GHZ")
        radio_page.enable(radio_page.get_wireless())
        radio_page.select_bandwidth(band)
        radio_page.set_channel(channel)
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "5 Ghz")
        wireless = radio_page.get_wireless()
        assertion.is_true(radio_page.is_enabled(wireless), "Wireless Enabled")
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
        time.sleep(120)  # DUT needs time to apply channel changes
        wifi_connection = network.wifi_connection(
            ssid=self.SSID, pswd=self.SSID_PASS, timeout=20)
        try:
            assertion.is_wificonnected(wifi_connection)
        except WifiConnError:
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
        ip = '192.168.0.1'
        wifi_iface = network.wifi_iface_name()  # get name of wifi iface
        ping_attempt = network.ping_attempt(wifi_iface, ip)
        try:
            assertion.is_sucessful(ping_attempt, "ping attempt")
        finally:
            network.connect_iface(eth_iface)
            self.reset_wifisession(self.firefox, self.SSID)
