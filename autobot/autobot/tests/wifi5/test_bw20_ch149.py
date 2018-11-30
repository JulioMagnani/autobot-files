from channel_parent import Channel

class TestBw20Ch149(Channel):
    
    def test_bw20_ch149(self, setUp):
        """Connect client to bandwidth 20/channel 149 5.0Ghz SSID"""

        self.common_channel(band='20', channel='149')