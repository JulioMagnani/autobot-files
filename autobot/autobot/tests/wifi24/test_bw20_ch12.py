from channel_parent import Channel

class TestBw20Ch12(Channel):

    def test_bw20_ch12(self, setUp):
        """Test bandwidth 20/channel 12 in 2.4Ghz interface"""

        self.common_channel(band='20', channel='12')