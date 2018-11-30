from channel_parent import Channel

class TestBw80Ch140(Channel):
    
    def test_bw80_ch140(self, setUp):
        """Connect client to bandwidth 80/channel 140 5.0Ghz SSID"""

        self.common_channel(band='80', channel='140/80')