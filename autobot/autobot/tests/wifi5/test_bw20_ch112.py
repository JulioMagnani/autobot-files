from channel_parent import Channel

class TestBw20Ch112(Channel):
    
    def test_bw20_ch112(self, setUp):
        """Connect client to bandwidth 20/channel 112 5.0Ghz SSID"""

        self.common_channel(band='20', channel='112')