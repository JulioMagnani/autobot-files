from channel_parent import Channel

class TestBw80Ch149(Channel):
    
    def test_bw80_ch149(self, setUp):
        """Connect client to bandwidth 80/channel 149 5.0Ghz SSID"""

        self.common_channel(band='80', channel='149/80')