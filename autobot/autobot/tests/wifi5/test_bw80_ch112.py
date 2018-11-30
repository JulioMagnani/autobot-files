from channel_parent import Channel

class TestBw80Ch112(Channel):
    
    def test_bw80_ch112(self, setUp):
        """Connect client to bandwidth 80/channel 112 5.0Ghz SSID"""

        self.common_channel(band='80', channel='112/80')