from channel_parent import Channel

class TestBw40Ch124(Channel):
    
    def test_bw40_ch124(self, setUp):
        """Connect client to bandwidth 40/channel 124 5.0Ghz SSID"""

        self.common_channel(band='40', channel='124')