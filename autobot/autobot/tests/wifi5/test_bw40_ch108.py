from channel_parent import Channel

class TestBw40Ch108(Channel):
    
    def test_bw40_ch108(self, setUp):
        """Connect client to bandwidth 40/channel 108 5.0Ghz SSID"""

        self.common_channel(band='40', channel='108')