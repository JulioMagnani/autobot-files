from channel_parent import Channel

class TestBw20Ch140(Channel):
    
    def test_bw20_ch140(self, setUp):
        """Connect client to bandwidth 20/channel 140 5.0Ghz SSID"""

        self.common_channel(band='20', channel='140')