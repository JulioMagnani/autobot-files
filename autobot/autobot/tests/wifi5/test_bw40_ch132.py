from channel_parent import Channel

class TestBw40Ch132(Channel):
    
    def test_bw40_ch132(self, setUp):
        """Connect client to bandwidth 40/channel 132 5.0Ghz SSID"""

        self.common_channel(band='40', channel='132')