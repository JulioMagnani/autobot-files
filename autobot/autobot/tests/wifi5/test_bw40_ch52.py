from channel_parent import Channel

class TestBw40Ch52(Channel):
    
    def test_bw40_ch52(self, setUp):
        """Connect client to bandwidth 40/channel 52 5.0Ghz SSID"""

        self.common_channel(band='40', channel='52')