from channel_parent import Channel

class TestBw40Ch60(Channel):
    
    def test_bw40_ch60(self, setUp):
        """Connect client to bandwidth 40/channel 60 5.0Ghz SSID"""

        self.common_channel(band='40', channel='60')