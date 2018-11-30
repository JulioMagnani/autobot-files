from channel_parent import Channel

class TestBw20Ch11(Channel):

    def test_bw20_ch11(self, setUp):
        """Test bandwidth 20/channel 11 in 2.4Ghz interface"""

        self.common_channel(band='20', channel='11')