from wifi24_parent import *

class PingScan(TestWifi24):

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