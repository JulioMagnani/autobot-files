from wifi24_parent import *

class DefaultEncryp(TestWifi24):

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