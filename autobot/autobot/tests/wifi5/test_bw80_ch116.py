from channel_parent import Channel

class TestBw80Ch116(Channel):
    
    def test_bw80_ch116(self, setUp):
        """Connect client to bandwidth 80/channel 116 5.0Ghz SSID"""

        self.common_channel(band='80', channel='116/80')