from channel_parent import Channel

class TestBw80Ch56(Channel):
    
    def test_bw80_ch56(self, setUp):
        """Connect client to bandwidth 80/channel 56 5.0Ghz SSID"""

        self.common_channel(band='80', channel='56/80')