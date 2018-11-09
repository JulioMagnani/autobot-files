from wifi5_parent import *

class LocalIpv6(TestWifi5):

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