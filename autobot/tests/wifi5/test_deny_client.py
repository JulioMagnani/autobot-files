from wifi5_parent import *

class DenyClient(TestWifi5):

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