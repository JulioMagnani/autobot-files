from wifi24_parent import *

class BroadcastOn(TestWifi24):

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