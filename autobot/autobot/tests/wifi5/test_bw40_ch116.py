from channel_parent import Channel

class TestBw40Ch116(Channel):
    
    def test_bw40_ch116(self, setUp):
        """Connect client to bandwidth 40/channel 116 5.0Ghz SSID"""

        self.common_channel(band='40', channel='116')