from channel_parent import Channel

class TestBw80Ch52(Channel):
    
    def test_bw80_ch52(self, setUp):
        """Connect client to bandwidth 80/channel 52 5.0Ghz SSID"""

        self.common_channel(band='80', channel='52/80')