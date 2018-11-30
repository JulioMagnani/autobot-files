from channel_parent import Channel

class TestBw20Ch128(Channel):
    
    def test_bw20_ch128(self, setUp):
        """Connect client to bandwidth 20/channel 128 5.0Ghz SSID"""

        self.common_channel(band='20', channel='128')