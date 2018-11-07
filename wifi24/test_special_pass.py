from wifi24_parent import *

class SpecialPass(TestWifi24):

    def test_special_pass(self):
        """Set custom key with special characters and connect WS to DUT
        """

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
        network_page.enable(network_page.get_wpa2())
        network_page.apply_changes()

        # assert primary network is enabled
        netwrk = network_page.get_primary_network()
        assertion.is_true(network_page.is_enabled(netwrk), 'Primary Network')
        wpa2 = network_page.get_wpa2()
        assertion.is_true(network_page.is_enabled(wpa2), 'WPA2 enabled')

        # set new passphrase "'?/#$%"&*()-+[]}{;:><,.|@
        new_pass = """"'?/#$%"&*()-+[]}{;:><,.|@"""
        network_page.set_password(new_pass)
        network_page.apply_changes()

        # assert passphrase was changed
        time.sleep(2)
        current_pass = network_page.get_password()
        assertion.is_equal(current_pass, new_pass)

        # connect using new passphrase
        connection_attempt = network.wifi_connection(
            ssid=self.SSID, pswd=new_pass, timeout=20)
        try:
            assertion.is_sucessful(connection_attempt, 'connection attempt')
        finally:
            self.reset_wifisession(self.firefox, self.SSID)

        # set new passphrase çáÁéÉ¡¿ñÑüÅåÄäÖğĞşŞÿóÓíÍúÜ
        network_page = NetworkPage(self.firefox)
        new_pass = """çáÁéÉ¡¿ñÑüÅåÄäÖğĞşŞÿóÓíÍúÜ"""
        network_page.set_password(new_pass)
        network_page.apply_changes()

        current_pass = network_page.get_password()
        try:
            assertion.not_equal(new_pass, current_pass)
        except ElementMatchError:
            radio_page = RadioPage(self.firefox)
            radio_page.reset_wireless_default()

        # set new passphrase ÚâÂêÊöØøßÆëËãÃõÕæ
        network_page = NetworkPage(self.firefox)
        new_pass = """ÚâÂêÊöØøßÆëËãÃõÕæ"""
        network_page.set_password(new_pass)
        network_page.apply_changes()

        current_pass = network_page.get_password()
        try:
            assertion.not_equal(new_pass, current_pass)
        except ElementMatchError:
            radio_page = RadioPage(self.firefox)
            radio_page.reset_wireless_default()