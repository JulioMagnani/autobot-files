from channel_parent import Channel

class TestBw20Ch10(Channel):

    def test_bw20_ch10(self, setUp):
        """Test bandwidth 20/channel 10 in 2.4Ghz interface"""

        self.common_channel(band='20', channel='10')
