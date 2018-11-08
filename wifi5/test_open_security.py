from wifi5_parent import *

class OpenSecurity(TestWifi5):

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