from channel_parent import Channel

class TestBw20Ch108(Channel):
    
    def test_bw20_ch108(self, setUp):
        """Connect client to bandwidth 20/channel 108 5.0Ghz SSID"""

        self.common_channel(band='20', channel='108')