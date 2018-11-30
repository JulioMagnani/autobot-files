from channel_parent import Channel

class TestBw20Ch116(Channel):
    
    def test_bw20_ch116(self, setUp):
        """Connect client to bandwidth 20/channel 116 5.0Ghz SSID"""

        self.common_channel(band='20', channel='116')