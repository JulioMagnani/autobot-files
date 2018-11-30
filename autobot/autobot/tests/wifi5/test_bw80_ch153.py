from channel_parent import Channel

class TestBw80Ch153(Channel):
    
    def test_bw80_ch153(self, setUp):
        """Connect client to bandwidth 80/channel 153 5.0Ghz SSID"""

        self.common_channel(band='80', channel='153/80')