from channel_parent import Channel

class TestBw20Ch120(Channel):
    
    def test_bw20_ch120(self, setUp):
        """Connect client to bandwidth 20/channel 120 5.0Ghz SSID"""

        self.common_channel(band='20', channel='120')