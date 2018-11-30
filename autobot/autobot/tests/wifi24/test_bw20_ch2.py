from channel_parent import Channel

class TestBw20Ch2(Channel):

    def test_bw20_ch2(self, setUp):
        """Test bandwidth 20/channel 2 in 2.4Ghz interface"""

        self.common_channel(band='20', channel='2')