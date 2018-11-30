from channel_parent import Channel

class TestBw40Ch157(Channel):
    
    def test_bw40_ch157(self, setUp):
        """Connect client to bandwidth 40/channel 157 5.0Ghz SSID"""

        self.common_channel(band='40', channel='157')