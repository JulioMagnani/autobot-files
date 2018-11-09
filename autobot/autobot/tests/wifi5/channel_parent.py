from wifi5_parent import *

class Channel(TestWifi5):

    def __init__(self):
        pass

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