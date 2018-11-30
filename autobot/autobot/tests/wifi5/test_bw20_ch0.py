from channel_parent import Channel

class TestBw20Ch0(Channel):
    
    def test_bw20_ch0(self, setUp):
        """Connect client to bandwidth 20/channel auto 5.0Ghz SSID"""

        self.common_channel(band='20', channel='0')