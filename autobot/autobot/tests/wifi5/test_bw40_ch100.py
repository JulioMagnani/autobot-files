from channel_parent import Channel

class TestBw40Ch100(Channel):
    
    def test_bw40_ch100(self, setUp):
        """Connect client to bandwidth 40/channel 100 5.0Ghz SSID"""

        self.common_channel(band='40', channel='100')