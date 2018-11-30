from channel_parent import Channel

class TestBw80Ch0(Channel):
    
    def test_bw80_ch0(self, setUp):
        """Connect client to bandwidth 80/channel auto 5.0Ghz SSID"""

        self.common_channel(band='80', channel='0/80')