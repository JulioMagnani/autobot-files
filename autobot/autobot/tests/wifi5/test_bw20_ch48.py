from channel_parent import Channel

class TestBw20Ch48(Channel):
    
    def test_bw20_ch48(self, setUp):
        """Connect client to bandwidth 20/channel 48 5.0Ghz SSID"""

        self.common_channel(band='20', channel='48')