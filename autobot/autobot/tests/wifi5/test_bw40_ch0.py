from channel_parent import Channel

class TestBw40Ch0(Channel):
    
    def test_bw40_ch0(self, setUp):
        """Connect client to bandwidth 40/channel auto 5.0Ghz SSID"""

        self.common_channel(band='40', channel='0')