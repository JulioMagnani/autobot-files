from wifi5_parent import *

class InternetAutoCh(TestWifi5):

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