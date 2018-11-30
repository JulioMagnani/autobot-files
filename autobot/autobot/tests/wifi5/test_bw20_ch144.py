from channel_parent import Channel

class TestBw20Ch144(Channel):
    
    def test_bw20_ch144(self, setUp):
        """Connect client to bandwidth 20/channel 144 5.0Ghz SSID"""

        self.common_channel(band='20', channel='144')