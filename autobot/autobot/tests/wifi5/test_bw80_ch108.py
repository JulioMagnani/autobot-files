from channel_parent import Channel

class TestBw80Ch108(Channel):
    
    def test_bw80_ch108(self, setUp):
        """Connect client to bandwidth 80/channel 108 5.0Ghz SSID"""

        self.common_channel(band='80', channel='108/80')