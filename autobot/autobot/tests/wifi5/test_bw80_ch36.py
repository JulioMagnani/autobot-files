from channel_parent import Channel

class TestBw80Ch36(Channel):
    
    def test_bw80_ch36(self, setUp):
        """Connect client to bandwidth 80/channel 36 5.0Ghz SSID"""

        self.common_channel(band='80', channel='36/80')