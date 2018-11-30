from channel_parent import Channel

class TestBw20Ch40(Channel):
    
    def test_bw20_ch40(self, setUp):
        """Connect client to bandwidth 20/channel 40 5.0Ghz SSID"""

        self.common_channel(band='20', channel='40')