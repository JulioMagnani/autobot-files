from channel_parent import Channel

class TestBw80Ch124(Channel):
    
    def test_bw80_ch124(self, setUp):
        """Connect client to bandwidth 80/channel 124 5.0Ghz SSID"""

        self.common_channel(band='80', channel='124/80')