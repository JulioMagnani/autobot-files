from channel_parent import Channel

class TestBw80Ch157(Channel):
    
    def test_bw80_ch157(self, setUp):
        """Connect client to bandwidth 80/channel 157 5.0Ghz SSID"""

        self.common_channel(band='80', channel='157/80')