from channel_parent import Channel

class TestBw80Ch132(Channel):
    
    def test_bw80_ch132(self, setUp):
        """Connect client to bandwidth 80/channel 132 5.0Ghz SSID"""

        self.common_channel(band='80', channel='132/80')