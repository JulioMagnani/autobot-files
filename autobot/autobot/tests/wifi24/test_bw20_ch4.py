from channel_parent import Channel

class TestBw20Ch4(Channel):

    def test_bw20_ch4(self, setUp):
        """Test bandwidth 20/channel 4 in 2.4Ghz interface"""

        self.common_channel(band='20', channel='4')