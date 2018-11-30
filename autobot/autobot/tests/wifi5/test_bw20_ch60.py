from channel_parent import Channel

class TestBw20Ch60(Channel):
    
    def test_bw20_ch60(self, setUp):
        """Connect client to bandwidth 20/channel 60 5.0Ghz SSID"""

        self.common_channel(band='20', channel='60')