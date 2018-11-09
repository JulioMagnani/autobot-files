from wifi24_parent import *

class Bandwidth(TestWifi24):

    def __init__(self):
        pass

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