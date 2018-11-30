from channel_parent import Channel

class TestBw80Ch64(Channel):
    
    def test_bw80_ch64(self, setUp):
        """Connect client to bandwidth 80/channel 64 5.0Ghz SSID"""

        self.common_channel(band='80', channel='64/80')