from wifi24_parent import *

class WPA2WrongPass(TestWifi24):
    
    def test_wpa2_wrongpass(self):
        """Attempt to connect to Wifi-WPA2 encryption AES with wrong password
        """

        network = conn()
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

        # enable both wpa2 and wpa
        network_page = NetworkPage(self.firefox)
        network_page.enable(network_page.get_primary_network())
        network_page.enable(network_page.get_wpa2())

        # Change WiFi password
        new_pass = 'Wpa2Change'
        network_page.set_password(new_pass)
        network_page.apply_changes()

        # check primary network and wpa2 are enabled and encryption is AES
        assertion.is_true(network_page.is_enabled(
                          network_page.get_primary_network()),
                          'Primary Network')
        assertion.is_true(network_page.is_enabled(
                          network_page.get_wpa2()), 'WPA2 enabled')
        assertion.is_equal(network_page.get_encryption(), 'AES')

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
