from wifi24_parent import *

class SSIDMaxChar(TestWifi24):

    def test_ssid_maxchar(self):
        """Check if DUT SSID name max characters allowed is 32
        """

        assertion = Assert()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable(radio_page.get_wireless())
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")

        wireless = radio_page.get_wireless()
        assertion.is_true(radio_page.is_enabled(wireless), "Wireless")

        # enable primary network, enable WPA2 and disable WPA
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.apply_changes()

        # Assert primary network is enabled
        netwrk = network_page.get_primary_network()
        assertion.is_true(network_page.is_enabled(netwrk), 'Primary Network')

        # Change SSID name to 40 characters then check ssid name length
        new_ssid = "NET_5G215F640000000000000000000001234567"
        network_page.set_ssid_name(new_ssid)
        network_page.apply_changes()

        # check length of ssid name equals maxlen 32
        ssid = network_page.get_ssid_name()
        try:
            assertion.is_true(ssid != self.SSID, "SSID was changed")
            assertion.is_equal(len(ssid), 32)
        finally:
            # reset wireless configuration
            radio_page = RadioPage(self.firefox)
            radio_page.reset_wireless_default()
