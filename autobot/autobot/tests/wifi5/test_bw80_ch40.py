from channel_parent import Channel

class TestBw80Ch40(Channel):
    
    def test_bw80_ch40(self, setUp):
        """Connect client to bandwidth 80/channel 40 5.0Ghz SSID"""

        self.common_channel(band='80', channel='40/80')