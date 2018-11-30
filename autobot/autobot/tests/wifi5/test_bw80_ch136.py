from channel_parent import Channel

class TestBw80Ch136(Channel):
    
    def test_bw80_ch136(self, setUp):
        """Connect client to bandwidth 80/channel 136 5.0Ghz SSID"""

        self.common_channel(band='80', channel='136/80')