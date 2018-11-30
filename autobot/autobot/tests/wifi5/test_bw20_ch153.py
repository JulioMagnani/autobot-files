from channel_parent import Channel

class TestBw20Ch153(Channel):
    
    def test_bw20_ch153(self, setUp):
        """Connect client to bandwidth 20/channel 153 5.0Ghz SSID"""

        self.common_channel(band='20', channel='153')