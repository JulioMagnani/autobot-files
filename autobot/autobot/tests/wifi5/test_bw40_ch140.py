from channel_parent import Channel

class TestBw40Ch140(Channel):
    
    def test_bw40_ch140(self, setUp):
        """Connect client to bandwidth 40/channel 140 5.0Ghz SSID"""

        self.common_channel(band='40', channel='140')