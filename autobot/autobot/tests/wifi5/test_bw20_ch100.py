from channel_parent import Channel

class TestBw20Ch100(Channel):
    
    def test_bw20_ch100(self, setUp):
        """Connect client to bandwidth 20/channel 100 5.0Ghz SSID"""

        self.common_channel(band='20', channel='100')