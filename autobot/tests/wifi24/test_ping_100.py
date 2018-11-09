from wifi24_parent import *

class Ping100(TestWifi24):

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
