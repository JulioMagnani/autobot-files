from channel_parent import Channel

class TestBw80Ch120(Channel):
    
    def test_bw80_ch120(self, setUp):
        """Connect client to bandwidth 80/channel 120 5.0Ghz SSID"""

        self.common_channel(band='80', channel='120/80')