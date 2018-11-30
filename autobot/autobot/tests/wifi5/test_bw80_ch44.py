from channel_parent import Channel

class TestBw80Ch44(Channel):
    
    def test_bw80_ch44(self, setUp):
        """Connect client to bandwidth 80/channel 44 5.0Ghz SSID"""

        self.common_channel(band='80', channel='44/80')