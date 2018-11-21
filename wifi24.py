import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from network import NetworkOps as conn
from autobot.PageObjects.security import SecurityPage
from autobot.PageObjects.login import LoginPage
from autobot.PageObjects.radio import RadioPage
from autobot.PageObjects.network import NetworkPage
from autobot.PageObjects.software import SoftwarePage
from autobot.exceptions import (NetworkError, WifiConnError, WebElementError,
                                SeleniumServerError, ElementMatchError)
from autobot.assertion import Assert


class TestWifi24(unittest.TestCase):

    USERNAME = None
    PASSWORD = None
    SSID = None
    SSID_PASS = None

    @classmethod
    def setUpClass(cls):
        try:
            cls.firefox = webdriver.Remote(
                desired_capabilities=DesiredCapabilities.FIREFOX)
        except Exception:
            raise SeleniumServerError(
                'Remote webdriver',
                'Could not reach selenium servers. Check docker!')

        login_page = LoginPage(cls.firefox)
        login_page.enter_credentials(cls.USERNAME, cls.PASSWORD)

    @classmethod
    def tearDownClass(cls):
        cls.firefox.quit()

    @classmethod
    def set_login(cls, login_info):
        cls.USERNAME = login_info['username']
        cls.PASSWORD = login_info['password']
        cls.SSID = login_info['ssid_2.4']
        cls.SSID_PASS = login_info['pass_2.4']

    @classmethod
    def reset_wifisession(cls, driver, ssid):
        conn().delete_wifi_profile(ssid=ssid)

        radio_page = RadioPage(driver)
        radio_page.reset_wireless_default()

        conn().reset_network_mngr()

    def suite(self, selected_tests):
        tests = selected_tests

        return unittest.TestSuite(map(TestWifi24, tests))

    def test_bw_20(self):
        """20MHz bandwidth connectivity from a client to the DUT"""

        self.__test_bandwidth(band='20')

    def test_bw_40(self):
        """40MHz bandwidth connectivity from a client to the DUT"""

        self.__test_bandwidth(band='40')

    def __test_bandwidth(self, band=None):
        """Test Bandwidth"""

        assertion = Assert()
        network = conn()

        # select wireless interface and bandwidth and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable_wireless()
        radio_page.select_bandwidth(band)
        radio_page.apply_changes()
        radio_page.refresh_page()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        assertion.is_equal(radio_page.wireless_isenabled(), "Enabled")
        assertion.is_equal(radio_page.get_bandwidth(), band)

        # enable primary network and wpa2
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.enable(network_page.get_wpa2())

        # check primary network and wpa2 are enabled
        assertion.is_true(network_page.is_enabled(
                          network_page.get_primary_network()),
                          'Primary Network')
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa2()), 'WPA 2')

        # wifi connection attempt
        time.sleep(3)
        wifi_connection = network.wifi_connection(ssid=self.SSID,
                                                  pswd=self.SSID_PASS)
        assertion.is_wificonnected(wifi_connection)

        # Disconnect wired interface
        eth_iface = network.eth_iface_name()  # get name of wired interface
        eth_disc_attempt = network.disconnect_iface(eth_iface)
        try:
            assertion.is_sucessful(eth_disc_attempt, 'ethernet disconnect')
        except NetworkError:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # ping attempt
        wifi_iface = network.wifi_iface_name()  # get name of wifi iface
        ip = '192.168.0.1'
        ping_attempt = network.ping_attempt(wifi_iface, ip)
        try:
            assertion.is_sucessful(ping_attempt, 'ping attempt')
        finally:
            network.connect_iface(eth_iface)
            self.reset_wifisession(self.firefox, self.SSID)

    def test_wpa_validpass(self):
        """Attempt to connect to Wifi-WPA with valid password"""

        network = conn()
        assertion = Assert()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable_wireless()
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        assertion.is_equal(radio_page.wireless_isenabled(), "Enabled")

        # enable primary network and both wpa2 and wpa
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.enable(network_page.get_wpa2())
        network_page.enable(network_page.get_wpa())

        # Set encryption to TKIP
        network_page.set_encryption("TKIP")

        # Change WiFi password
        new_pass = 'WpaPskChange'
        network_page.set_password(new_pass)

        network_page.apply_changes()

        # check wpa-psk is enabled and encryption is TKIP
        assertion.is_true(network_page.is_enabled(
                          network_page.get_primary_network()),
                          'Primary Network')
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa()), 'WPA enabled')
        assertion.is_equal(network_page.get_encryption(), 'TKIP+AES')

        # check password is 'WpaPskChange'
        assertion.is_equal(network_page.get_password(), new_pass)

        # Wifi connection attempt
        time.sleep(20)
        connection_attempt = network.wifi_connection(ssid=self.SSID,
                                                     pswd=new_pass)
        try:
            assertion.is_sucessful(connection_attempt, 'connection attempt')
        except NetworkError:
            self.reset_wifisession(self.firefox, self.SSID_PASS)
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
        ping_attempt = network.ping_attempt(wifi_iface, ip)
        try:
            assertion.is_sucessful(ping_attempt, 'ping attempt')
        finally:
            network.connect_iface(eth_name)
            self.reset_wifisession(self.firefox, self.SSID)

    def test_wpa_wrongpass(self):
        """Attempt to connect to Wifi-WPA with wrong password"""

        network = conn()
        assertion = Assert()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable_wireless()
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        assertion.is_equal(radio_page.wireless_isenabled(), "Enabled")

        # enable primary network and both wpa2 and wpa
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.enable(network_page.get_wpa2())
        network_page.enable(network_page.get_wpa())

        # Set encryption to TKIP
        network_page.set_encryption("TKIP")

        # Change WiFi password
        new_pass = 'WpaChange'
        network_page.set_password(new_pass)

        network_page.apply_changes()

        # check wpa-psk is enabled and encryption is TKIP
        assertion.is_true(network_page.is_enabled(
                          network_page.get_primary_network()),
                          'Primary Network')
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa()), 'WPA enabled')
        assertion.is_equal(network_page.get_encryption(), 'TKIP+AES')

        # check password is 'WpaPskChange'
        assertion.is_equal(network_page.get_password(), new_pass)

        # Wifi connection attempt
        time.sleep(20)
        connection_attempt = network.wifi_connection(ssid=self.SSID,
                                                     pswd='WrongPass')
        try:
            assertion.is_unsucessful(connection_attempt, 'connection attempt')
        finally:
            self.reset_wifisession(self.firefox, self.SSID)

    def test_wpa2_validpass(self):
        """Connect to Wifi-WPA2 encryption AES with valid password"""

        network = conn()
        assertion = Assert()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable_wireless()
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        assertion.is_equal(radio_page.wireless_isenabled(), "Enabled")

        # enable wpa2
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.enable(network_page.get_wpa2())

        # Change WiFi password
        new_pass = 'Wpa2Change'
        network_page.set_password(new_pass)

        network_page.apply_changes()

        # check primary network and wpa2 are enabled and encryption is AES
        assertion.is_true(network_page.is_enabled(
                          network_page.get_primary_network()),
                          'Primary Network')
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa2()), 'WPA2 enabled')
        assertion.is_equal(network_page.get_encryption(), 'AES')

        # check password is 'Wpa2Change'
        assertion.is_equal(network_page.get_password(), new_pass)

        # Wifi connection attempt
        time.sleep(20)
        connection_attempt = network.wifi_connection(ssid=self.SSID,
                                                     pswd=new_pass)
        try:
            assertion.is_sucessful(connection_attempt, 'connection attempt')
        except NetworkError:
            self.reset_wifisession(self.firefox, self.SSID)  # reset wifi/DUT
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
        ping_attempt = network.ping_attempt(wifi_iface, ip)
        try:
            assertion.is_sucessful(ping_attempt, 'ping attempt')
        finally:
            network.connect_iface(eth_name)
            self.reset_wifisession(self.firefox, self.SSID)

    def test_wpa2_wrongpass(self):
        """Attempt to connect to Wifi-WPA2 encryption AES with wrong password
        """

        network = conn()
        assertion = Assert()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable(radio_page.get_wireless())
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        wireless = radio_page.get_wireless()
        assertion.is_true(radio_page.is_enabled(wireless), "Wireless")

        # enable both wpa2 and wpa
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.enable(network_page.get_wpa2())

        # Change WiFi password
        new_pass = 'Wpa2Change'
        network_page.set_password(new_pass)
        network_page.apply_changes()

        # check primary network and wpa2 are enabled and encryption is AES
        assertion.is_true(network_page.is_enabled(
                          network_page.get_primary_network()),
                          'Primary Network')
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa2()), 'WPA2 enabled')
        assertion.is_equal(network_page.get_encryption(), 'AES')

        # check password is 'WpaPskChange'
        assertion.is_equal(network_page.get_password(), new_pass)

        # Wifi connection attempt
        time.sleep(20)
        connection_attempt = network.wifi_connection(ssid=self.SSID,
                                                     pswd='WrongPass')
        try:
            assertion.is_unsucessful(connection_attempt, 'connection attempt')
        finally:
            self.reset_wifisession(self.firefox, self.SSID)

    def test_custom_key(self):
        """Set new key passphrase then connect WS to DUT.
        """

        network = conn()
        assertion = Assert()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable_wireless()
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        assertion.is_equal(radio_page.wireless_isenabled(), "Enabled")

        # enable primary network, enable WPA2 and disable WPA
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.enable(network_page.get_wpa2())
        network_page.disable(network_page.get_wpa())
        network_page.apply_changes()

        # Assert only WPA2 is enabled
        assertion.is_true(network_page.is_enabled(
                          network_page.get_primary_network()),
                          'Primary Network')
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa2()), 'WPA 2')
        assertion.is_false(network_page.is_enabled(
                           network_page.get_wpa()), 'WPA')

        # change key passphrase to '1234567890'
        password = '1234567890'
        network_page.set_password(password)
        network_page.apply_changes()

        # assert password was changed
        assertion.is_equal(network_page.get_password(), password)

        # Wifi connection attempt
        network.reset_network_mngr()
        wifi_connection = network.wifi_connection(
            ssid=self.SSID, pswd=password, timeout=20)
        try:
            assertion.is_wificonnected(wifi_connection)
        except WifiConnError:
            self.reset_wifisession(self.firefox, self.SSID)
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
        wifi_iface = network.wifi_iface_name()  # get name of wifi iface
        ip = 'www.google.com'
        time.sleep(10)
        ping_attempt = network.ping_attempt(wifi_iface, ip)
        time.sleep(10)
        try:
            assertion.is_sucessful(ping_attempt, "ping attempt")
        finally:
            network.connect_iface(eth_iface)
            self.reset_wifisession(self.firefox, self.SSID)

        # enable wpa
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_wpa())

        # Set encryption to TKIP
        network_page.set_encryption("TKIP")

        # Change WiFi password
        new_pass = 'NEW1234567890'
        network_page.set_password(new_pass)
        network_page.apply_changes()

        # check wpa-psk is enabled and encryption is TKIP
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa()), 'WPA is enabled')
        assertion.is_equal(network_page.get_encryption(), 'TKIP+AES')

        # check password is 'WpaPskChange'
        assertion.is_equal(network_page.get_password(), new_pass)

        # Wifi connection attempt
        network.reset_network_mngr()
        wifi_connection = network.wifi_connection(
            ssid=self.SSID, pswd=new_pass, timeout=20)
        try:
            assertion.is_wificonnected(wifi_connection)
        except WifiConnError:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # Disconnect wired interface
        eth_disc_attempt = network.disconnect_iface(eth_iface)
        try:
            assertion.is_sucessful(eth_disc_attempt, "ethernet disconnect")
        except NetworkError:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # ping attempt
        ip = 'www.google.com'
        ping_attempt = network.ping_attempt(wifi_iface, ip)
        try:
            assertion.is_sucessful(ping_attempt, "ping attempt")
        finally:
            network.connect_iface(eth_iface)
            self.reset_wifisession(self.firefox, self.SSID)

    def test_open_sec(self):
        """Connect station to open wifi network"""

        network = conn()
        assertion = Assert()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable_wireless()
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        assertion.is_equal(radio_page.wireless_isenabled(), "Enabled")

        # disable WPA2
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.disable(network_page.get_wpa2())
        network_page.apply_changes()

        # assert WPA2 (therefore WPA too for 3P Box) is disabled
        assertion.is_true(network_page.is_enabled(
                          network_page.get_primary_network()),
                          'Primary Network')
        assertion.is_false(network_page.is_enabled(
                           network_page.get_wpa2()), 'WPA 2')

        # Wifi connection attempt
        network.reset_network_mngr()
        time.sleep(5)
        wifi_connection = network.wifi_connection_nosec(ssid=self.SSID)
        try:
            assertion.is_wificonnected(wifi_connection)
        except WifiConnError:
            self.reset_wifisession(self.firefox, self.SSID)
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
        wifi_iface = network.wifi_iface_name()  # get name of wifi iface
        ip = 'www.google.com'
        ping_attempt = network.ping_attempt(wifi_iface, ip)
        try:
            assertion.is_sucessful(ping_attempt, "ping attempt")
        finally:
            network.connect_iface(eth_iface)
            self.reset_wifisession(self.firefox, self.SSID)

    def test_deny_opensec(self):
        """DUT denies access to client without password"""

        network = conn()
        assertion = Assert()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable_wireless()
        radio_page.apply_changes()

        # assert wireless is enabled and bandwidth is 2.4Ghz
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        assertion.is_equal(radio_page.wireless_isenabled(), "Enabled")

        # enable Primary Network and WPA2 and disable WPA
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.enable(network_page.get_wpa2())
        network_page.disable(network_page.get_wpa())
        network_page.apply_changes()

        # Assert only WPA2 is enabled
        assertion.is_true(network_page.is_enabled(
                          network_page.get_primary_network()),
                          'Primary Network')
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa2()), 'WPA 2')
        assertion.is_false(network_page.is_enabled(
                          network_page.get_wpa()), 'WPA')

        # Wifi connection attempt
        network.reset_network_mngr()
        wifi_connection = network.wifi_connection_nosec(ssid=self.SSID)
        try:
            assertion.is_false(wifi_connection, 'wifi connection')
        finally:
            self.reset_wifisession(self.firefox, self.SSID)

        # enable wpa and set encryption to TKIP
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_wpa())
        network_page.set_encryption("TKIP")
        network_page.apply_changes()

        # check wpa-psk is enabled and encryption is TKIP
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa()), 'WPA is enabled')
        assertion.is_equal(network_page.get_encryption(), 'TKIP+AES')

        # Wifi connection attempt
        network.reset_network_mngr()
        wifi_connection = network.wifi_connection_nosec(ssid=self.SSID)
        try:
            assertion.is_false(wifi_connection, 'wifi connection')
        finally:
            self.reset_wifisession(self.firefox, self.SSID)

        # disable WPA2
        network_page = NetworkPage(self.firefox)
        network_page.disable(network_page.get_wpa2())
        network_page.apply_changes()

        # assert WPA2 (therefore WPA too for 3P Box) is disabled
        assertion.is_false(network_page.is_enabled(
                           network_page.get_wpa2()), 'WPA 2')

        # Wifi connection attempt
        network.reset_network_mngr()
        time.sleep(5)
        wifi_connection = network.wifi_connection_nosec(ssid=self.SSID)
        try:
            assertion.is_wificonnected(wifi_connection)
        finally:
            self.reset_wifisession(self.firefox, self.SSID)

    def test_ssid_maxchar(self):
        """Check if DUT SSID name max characters allowed is 32
        """

        assertion = Assert()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable(radio_page.get_wireless())
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")

        wireless = radio_page.get_wireless()
        assertion.is_true(radio_page.is_enabled(wireless), "Wireless")

        # enable primary network, enable WPA2 and disable WPA
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.apply_changes()

        # Assert primary network is enabled
        netwrk = network_page.get_primary_network()
        assertion.is_true(network_page.is_enabled(netwrk), 'Primary Network')

        # Change SSID name to 40 characters then check ssid name length
        new_ssid = "NET_5G215F640000000000000000000001234567"
        network_page.set_ssid_name(new_ssid)
        network_page.apply_changes()

        # check length of ssid name equals maxlen 32
        ssid = network_page.get_ssid_name()
        try:
            assertion.is_true(ssid != self.SSID, "SSID was changed")
            assertion.is_equal(len(ssid), 32)
        finally:
            # reset wireless configuration
            radio_page = RadioPage(self.firefox)
            radio_page.reset_wireless_default()

    def test_wpa2_to_wpa(self):
        """Connect WS to DUT then change sec wpa2 to wpa/wpa2
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

        # enable primary network and wpa2 and disable wpa
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.enable(network_page.get_wpa2())
        network_page.disable(network_page.get_wpa())

        network_page.apply_changes()

        # check primary network and wpa2 are enabled and encryption is AES
        netwrk = network_page.get_primary_network()
        assertion.is_true(network_page.is_enabled(netwrk), 'Primary Network')
        wpa2 = network_page.get_wpa2()
        assertion.is_true(network_page.is_enabled(wpa2), 'WPA2 enabled')
        wpa = network_page.get_wpa()
        assertion.is_false(network_page.is_enabled(wpa), 'WPA disabled')

        # Wifi connection attempt
        network.reset_network_mngr()
        wifi_connection = network.wifi_connection(
            ssid=self.SSID, pswd=self.SSID_PASS, timeout=20)
        try:
            assertion.is_wificonnected(wifi_connection)
        except WifiConnError:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # enable wpa
        time.sleep(30)
        network_page.enable(network_page.get_wpa())

        # Set encryption to TKIP
        network_page.set_encryption("TKIP")

        network_page.apply_changes()

        # check wpa-psk is enabled and encryption is TKIP
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa()), 'WPA is enabled')
        assertion.is_equal(network_page.get_encryption(), 'TKIP+AES')

        # Disconnect wired interface
        eth_iface = network.eth_iface_name()  # get name of wired iface
        eth_disc_attempt = network.disconnect_iface(eth_iface)
        try:
            assertion.is_sucessful(eth_disc_attempt, "ethernet disconnect")
        except NetworkError:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # ping attempt
        ip = 'www.google.com'
        wifi_iface = network.wifi_iface_name()  # get name of wifi iface
        ping_attempt = network.ping_attempt(wifi_iface, ip)
        try:
            assertion.is_sucessful(ping_attempt, "ping attempt")
        finally:
            network.connect_iface(eth_iface)
            self.reset_wifisession(self.firefox, self.SSID)

    def test_ssid_newname(self):
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
        new_ssid = new_ssid = "{0}NEWSSIDNAME".format(self.SSID)
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

    def test_nmode_auto(self):
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

    def test_nmode_off(self):
        """WiFi Client can ping gateway's local addr with 802.11 n-mode off"""

        assertion = Assert()
        network = conn()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable(radio_page.get_wireless())
        radio_page.disable(radio_page.get_n_mode())
        radio_page.apply_changes()

        # assert wireless is enabled and interface is 2.4Ghz
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        assertion.is_false(radio_page.is_nmode_enabled(), 'N MODE')
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

    def test_ping_100(self):
        """Wlan host ping Gateway LAN IP with 100% success"""

        assertion = Assert()
        network = conn()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable(radio_page.get_wireless())
        radio_page.apply_changes()

        # assert wireless is enabled and interface is 2.4Ghz
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        wireless = radio_page.get_wireless()
        assertion.is_true(radio_page.is_enabled(wireless), "Wireless")

        # enable primary network
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())

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
        eth_name = network.eth_iface_name()
        eth_disc_attempt = network.disconnect_iface(eth_name)
        try:
            assertion.is_sucessful(eth_disc_attempt, 'wired disconnection')
        except NetworkError:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # 10 Ping attempt to get 100% of success
        time.sleep(3)
        wifi_iface = network.wifi_iface_name()  # get wifi iface name
        DUT_default_IP = '192.168.0.1'
        ping_attempt = network.ping_attempt_100(
                wifi_iface, DUT_default_IP, count=10)
        try:
            assertion.is_sucessful(ping_attempt, 'ping attempt')
        finally:
            # reconfigure network interfaces to original settings
            network.connect_iface(eth_name)
            self.reset_wifisession(self.firefox, self.SSID)

    def test_ping_scan(self):
        """Ping (fixed channel) while doing network scan"""

        assertion = Assert()
        network = conn()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable(radio_page.get_wireless())
        radio_page.select_bandwidth('20')
        radio_page.set_channel('1')
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        wireless = radio_page.get_wireless()
        assertion.is_true(radio_page.is_enabled(wireless), "Wireless")
        assertion.is_equal(radio_page.get_bandwidth(), '20')
        assertion.is_equal(radio_page.get_channel(), '1')

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
        eth_name = network.eth_iface_name()  # get name of wired iface
        eth_disc_attempt = network.disconnect_iface(eth_name)
        try:
            assertion.is_sucessful(eth_disc_attempt, "ethernet disconnect")
        except NetworkError:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # Click on scan button
        time.sleep(3)
        radio_page = RadioPage(self.firefox)
        try:
            radio_page.click_on_scan()
        except Exception:
            network.connect_iface(eth_name)
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # 10 Ping attempt to get 100% of success
        time.sleep(3)
        wifi_iface = network.wifi_iface_name()  # get wifi iface name
        DUT_default_IP = '192.168.0.1'
        ping_attempt = network.ping_attempt_100(
                wifi_iface, DUT_default_IP, count=10)
        time.sleep(10)
        try:
            assertion.is_sucessful(ping_attempt, 'ping attempt')
        finally:
            # reconfigure network interfaces to original settings
            network.connect_iface(eth_name)
            self.reset_wifisession(self.firefox, self.SSID)

    def test_ping_scan_auto(self):
        """Ping (auto channel) nmode off while doing network scan"""

        assertion = Assert()
        network = conn()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable(radio_page.get_wireless())

        # set channel auto, band 20 and disable n mode
        radio_page.select_bandwidth('20')
        radio_page.set_channel('0')
        radio_page.disable(radio_page.get_n_mode())
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        wireless = radio_page.get_wireless()
        assertion.is_true(radio_page.is_enabled(wireless), "Wireless")
        assertion.is_equal(radio_page.get_bandwidth(), '20')
        assertion.is_equal(radio_page.get_channel(), '0')
        assertion.is_false(radio_page.is_nmode_enabled(), "N Mode")

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
        eth_name = network.eth_iface_name()  # get name of wired iface
        eth_disc_attempt = network.disconnect_iface(eth_name)
        try:
            assertion.is_sucessful(eth_disc_attempt, "ethernet disconnect")
        except NetworkError:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # Click on scan button
        time.sleep(3)
        radio_page = RadioPage(self.firefox)
        try:
            radio_page.click_on_scan()
        except Exception:
            network.connect_iface(eth_name)
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # 10 Ping attempt to get 100% of success
        time.sleep(3)
        wifi_iface = network.wifi_iface_name()  # get wifi iface name
        DUT_default_IP = '192.168.0.1'
        ping_attempt = network.ping_attempt_100(
                wifi_iface, DUT_default_IP, count=10)
        time.sleep(10)
        try:
            assertion.is_sucessful(ping_attempt, 'ping attempt')
        finally:
            # reconfigure network interfaces to original settings
            network.connect_iface(eth_name)
            self.reset_wifisession(self.firefox, self.SSID)

    def test_internet_fix_ch(self):
        """Test internet connection w fixed channel"""

        self.__test_channel(band='20', channel='1', url='www.google.com')

    def test_wps_isenabled(self):
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
        assertion.is_true(network_page.is_enabled(wps), 'WPS')

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="5.0GHZ")
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "5 Ghz")

        # assert wps is enabled
        network_page = NetworkPage(self.firefox)
        wps = network_page.get_wps()
        assertion.is_true(network_page.is_enabled(wps), 'WPS')

    def test_special_pass(self):
        """Set custom key with special characters and connect WS to DUT
        """

        assertion = Assert()
        network = conn()

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
        network_page.enable(network_page.get_wpa2())
        network_page.apply_changes()

        # assert primary network is enabled
        netwrk = network_page.get_primary_network()
        assertion.is_true(network_page.is_enabled(netwrk), 'Primary Network')
        wpa2 = network_page.get_wpa2()
        assertion.is_true(network_page.is_enabled(wpa2), 'WPA2 enabled')

        # set new passphrase "'?/#$%"&*()-+[]}{;:><,.|@
        new_pass = """"'?/#$%"&*()-+[]}{;:><,.|@"""
        network_page.set_password(new_pass)
        network_page.apply_changes()

        # assert passphrase was changed
        time.sleep(2)
        current_pass = network_page.get_password()
        assertion.is_equal(current_pass, new_pass)

        # connect using new passphrase
        connection_attempt = network.wifi_connection(
            ssid=self.SSID, pswd=new_pass, timeout=20)
        try:
            assertion.is_sucessful(connection_attempt, 'connection attempt')
        finally:
            self.reset_wifisession(self.firefox, self.SSID)

        # set new passphrase çáÁéÉ¡¿ñÑüÅåÄäÖğĞşŞÿóÓíÍúÜ
        network_page = NetworkPage(self.firefox)
        new_pass = """çáÁéÉ¡¿ñÑüÅåÄäÖğĞşŞÿóÓíÍúÜ"""
        network_page.set_password(new_pass)
        network_page.apply_changes()

        current_pass = network_page.get_password()
        try:
            assertion.not_equal(new_pass, current_pass)
        except ElementMatchError:
            radio_page = RadioPage(self.firefox)
            radio_page.reset_wireless_default()

        # set new passphrase ÚâÂêÊöØøßÆëËãÃõÕæ
        network_page = NetworkPage(self.firefox)
        new_pass = """ÚâÂêÊöØøßÆëËãÃõÕæ"""
        network_page.set_password(new_pass)
        network_page.apply_changes()

        current_pass = network_page.get_password()
        try:
            assertion.not_equal(new_pass, current_pass)
        except ElementMatchError:
            radio_page = RadioPage(self.firefox)
            radio_page.reset_wireless_default()

    def test_default_encryp(self):
        """ Test default Encryption WPA2-PSK/AES - Transfer data"""

        assertion = Assert()
        network = conn()

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

        # Assert if WPA is disabled as default
        network_page = NetworkPage(self.firefox)
        wpa = network_page.get_wpa()
        assertion.is_false(network_page.is_enabled(wpa), "WPA disabled")

        # Assert if WPA2 is enabled as defaul
        wpa2 = network_page.get_wpa2()
        assertion.is_true(network_page.is_enabled(wpa2), "WPA2 enabled")

        # Assert if AES encryption mode is enabled as default
        encrypt = network_page.get_encryption()
        assertion.is_equal(encrypt, 'AES')

        # wifi connection attempt
        wifi_conn_attempt = network.wifi_connection(
            ssid=self.SSID, pswd=self.SSID_PASS, timeout=20)
        assertion.is_wificonnected(wifi_conn_attempt)

        # disconnect ethernet interface
        try:
            eth_iface = network.eth_iface_name()
            eth_disc_attempt = network.disconnect_iface(eth_iface)
            assertion.is_true(eth_disc_attempt, "Disconnect ethernet")
        except Exception:
            self.reset_wifisession(self.firefox, self.SSID)
            raise

        # Transfer data between Wlan client and DUT
        time.sleep(3)
        url = '192.168.0.1'
        try:
            data_transf = network.transfer_data(url)
            assertion.is_true(data_transf, 'Data Transfer')
        finally:
            # reconfigure network interfaces to original settings
            network.connect_iface(eth_iface)
            self.reset_wifisession(self.firefox, self.SSID)

    def test_broadcast_on(self):
        """Verify enabled SSID broadcast status"""

        assertion = Assert()
        network = conn()

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

        # assert primary network is enabled
        netwrk = network_page.get_primary_network()
        assertion.is_true(network_page.is_enabled(netwrk), 'Primary Network')

        # Check if ssid shows up on wifi scan
        wifi_24_ssid = network_page.get_ssid_name()
        ssid_online = network.ssid_check(ssid=wifi_24_ssid)
        assertion.is_true(ssid_online, "SSID is online")

    def test_broadcast_off(self):
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
            assertion.is_true(ssid_online, "SSID is offline")
        finally:
            # reset changes
            radio_page = RadioPage(self.firefox)
            radio_page.reset_wireless_default()

    # ========================================================
    # ================  WIFI CHANNELS  =======================
    # ========================================================
    def test_bw20_ch1(self):
        """Test bandwidth 20/channel 1 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='1')

    def test_bw20_ch2(self):
        """Test bandwidth 20/channel 2 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='2')

    def test_bw20_ch3(self):
        """Test bandwidth 20/channel 3 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='3')

    def test_bw20_ch4(self):
        """Test bandwidth 20/channel 4 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='4')

    def test_bw20_ch5(self):
        """Test bandwidth 20/channel 5 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='5')

    def test_bw20_ch6(self):
        """Test bandwidth 20/channel 6 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='6')

    def test_bw20_ch7(self):
        """Test bandwidth 20/channel 7 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='7')

    def test_bw20_ch8(self):
        """Test bandwidth 20/channel 8 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='8')

    def test_bw20_ch9(self):
        """Test bandwidth 20/channel 9 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='9')

    def test_bw20_ch10(self):
        """Test bandwidth 20/channel 10 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='10')

    def test_bw20_ch11(self):
        """Test bandwidth 20/channel 11 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='11')

    def test_bw20_ch12(self):
        """Test bandwidth 20/channel 12 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='12')

    def test_bw20_ch13(self):
        """Test bandwidth 20/channel 13 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='13')

    def test_bw20_auto(self):
        """Test bandwidth 20/channel auto in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='0')

    def test_bw40_ch1(self):
        """Test bandwidth 40/channel 1 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='1')

    def test_bw40_ch2(self):
        """Test bandwidth 40/channel 2 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='2')

    def test_bw40_ch3(self):
        """Test bandwidth 40/channel 3 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='3')

    def test_bw40_ch4(self):
        """Test bandwidth 40/channel 4 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='4')

    def test_bw40_ch5(self):
        """Test bandwidth 40/channel 5 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='5')

    def test_bw40_ch6(self):
        """Test bandwidth 40/channel 6 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='6')

    def test_bw40_ch7(self):
        """Test bandwidth 40/channel 7 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='7')

    def test_bw40_ch8(self):
        """Test bandwidth 40/channel 8 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='8')

    def test_bw40_ch9(self):
        """Test bandwidth 40/channel 9 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='9')

    def test_bw40_auto(self):
        """Test bandwidth 40/channel auto in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='0')

    def __test_channel(self, band=None, channel=None, url='192.168.0.1'):
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
