from channel_parent import Channel

class TestBw80Ch60(Channel):
    
    def test_bw80_ch60(self, setUp):
        """Connect client to bandwidth 80/channel 60 5.0Ghz SSID"""

        self.common_channel(band='80', channel='60/80')