from channel_parent import Channel

class TestBw80Ch48(Channel):
    
    def test_bw80_ch48(self, setUp):
        """Connect client to bandwidth 80/channel 48 5.0Ghz SSID"""

        self.common_channel(band='80', channel='48/80')