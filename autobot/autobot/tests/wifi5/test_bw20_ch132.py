from channel_parent import Channel

class TestBw20Ch132(Channel):
    
    def test_bw20_ch132(self, setUp):
        """Connect client to bandwidth 20/channel 132 5.0Ghz SSID"""

        self.common_channel(band='20', channel='132')