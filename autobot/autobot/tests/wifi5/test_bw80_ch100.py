from channel_parent import Channel

class TestBw80Ch100(Channel):
    
    def test_bw80_ch100(self, setUp):
        """Connect client to bandwidth 80/channel 100 5.0Ghz SSID"""

        self.common_channel(band='80', channel='100/80')