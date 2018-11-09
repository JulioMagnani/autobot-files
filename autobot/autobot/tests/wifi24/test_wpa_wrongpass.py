from wifi24_parent import *

class WPAWrongPass(TestWifi24):

    def test_wpa_wrongpass(self):
        """Attempt to connect to Wifi-WPA with wrong password"""

        network = conn()
        assertion = Assert()

        # select wireless interface and enable wireless
        radio_page = RadioPage(self.firefox)
        radio_page.select_wifi_interface(iface="2.4GHZ")
        radio_page.enable_wireless()
        radio_page.apply_changes()

        # assert wireless and bandwidth
        assertion.is_equal(radio_page.get_wifi_interface(), "2.4 Ghz")
        assertion.is_equal(radio_page.wireless_isenabled(), "Enabled")

        # enable primary network and both wpa2 and wpa
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.enable(network_page.get_wpa2())
        network_page.enable(network_page.get_wpa())

        # Set encryption to TKIP
        network_page.set_encryption("TKIP")

        # Change WiFi password
        new_pass = 'WpaChange'
        network_page.set_password(new_pass)

        network_page.apply_changes()

        # check wpa-psk is enabled and encryption is TKIP
        assertion.is_true(network_page.is_enabled(
                          network_page.get_primary_network()),
                          'Primary Network')
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa()), 'WPA enabled')
        assertion.is_equal(network_page.get_encryption(), 'TKIP+AES')

        # check password is 'WpaPskChange'
        assertion.is_equal(network_page.get_password(), new_pass)

        # Wifi connection attempt
        time.sleep(20)
        connection_attempt = network.wifi_connection(ssid=self.SSID,
                                                     pswd='WrongPass')
        try:
            assertion.is_unsucessful(connection_attempt, 'connection attempt')
        finally:
            self.reset_wifisession(self.firefox, self.SSID)
