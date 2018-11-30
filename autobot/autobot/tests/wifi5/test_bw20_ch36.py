from channel_parent import Channel

class TestBw20Ch36(Channel):
    
    def test_bw20_ch36(self, setUp):
        """Connect client to bandwidth 20/channel 36 5.0Ghz SSID"""

        self.common_channel(band='20', channel='36')