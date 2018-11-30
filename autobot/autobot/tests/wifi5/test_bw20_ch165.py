from channel_parent import Channel

class TestBw20Ch165(Channel):
    
    def test_bw20_ch165(self, setUp):
        """Connect client to bandwidth 20/channel 165 5.0Ghz SSID"""

        self.common_channel(band='20', channel='165')