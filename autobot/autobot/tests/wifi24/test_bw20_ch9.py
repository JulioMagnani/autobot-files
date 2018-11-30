from channel_parent import Channel

class TestBw20Ch9(Channel):

    def test_bw20_ch9(self, setUp):
        """Test bandwidth 20/channel 9 in 2.4Ghz interface"""

        self.common_channel(band='20', channel='9')