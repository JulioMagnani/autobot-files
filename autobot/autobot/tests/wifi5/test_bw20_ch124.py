from channel_parent import Channel

class TestBw20Ch124(Channel):
    
    def test_bw20_ch124(self, setUp):
        """Connect client to bandwidth 20/channel 124 5.0Ghz SSID"""

        self.common_channel(band='20', channel='124')