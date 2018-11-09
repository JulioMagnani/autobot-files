from wifi24_parent import *

class BroadcastOff(TestWifi24):

    def test_broadcast_off(self):
        """ Verify disabled SSID broadcast status"""

        assertion = Assert()
        network = conn()

        # select wireless interface and disable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.disable(radio_page.get_wireless())
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        wireless = radio_page.get_wireless()
        assertion.is_false(radio_page.is_enabled(wireless), "Wireless")

        # disable primary network
        network_page = NetworkPage(self.firefox)
        network_page.disable(network_page.get_primary_network())
        network_page.apply_changes()

        # assert primary network is enabled
        netwrk = network_page.get_primary_network()
        assertion.is_false(network_page.is_enabled(netwrk), 'Primary Network')

        # Check if ssid shows up on wifi scan
        wifi_24_ssid = network_page.get_ssid_name()
        ssid_online = network.ssid_check(ssid=wifi_24_ssid)
        try:
            assertion.is_true(ssid_online, "SSID is offline")
        finally:
            # reset changes
            radio_page = RadioPage(self.firefox)
            radio_page.reset_wireless_default()