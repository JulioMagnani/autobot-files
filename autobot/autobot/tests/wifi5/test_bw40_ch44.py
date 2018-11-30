from channel_parent import Channel

class TestBw40Ch44(Channel):
    
    def test_bw40_ch44(self, setUp):
        """Connect client to bandwidth 40/channel 44 5.0Ghz SSID"""

        self.common_channel(band='40', channel='44')