from channel_parent import Channel

class TestBw40Ch36(Channel):
    
    def test_bw40_ch36(self, setUp):
        """Connect client to bandwidth 40/channel 36 5.0Ghz SSID"""

        self.common_channel(band='40', channel='36')