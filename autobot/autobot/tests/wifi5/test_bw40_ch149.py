from channel_parent import Channel

class TestBw40Ch149(Channel):
    
    def test_bw40_ch149(self, setUp):
        """Connect client to bandwidth 40/channel 149 5.0Ghz SSID"""

        self.common_channel(band='40', channel='149')