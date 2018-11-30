from channel_parent import Channel

class TestBw80Ch161(Channel):
    
    def test_bw80_ch161(self, setUp):
        """Connect client to bandwidth 80/channel 161 5.0Ghz SSID"""

        self.common_channel(band='80', channel='161/80')