from channel_parent import Channel

class TestBw80Ch128(Channel):
    
    def test_bw80_ch128(self, setUp):
        """Connect client to bandwidth 80/channel 128 5.0Ghz SSID"""

        self.common_channel(band='80', channel='128/80')