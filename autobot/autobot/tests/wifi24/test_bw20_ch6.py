from channel_parent import Channel

class TestBw20Ch6(Channel):

    def test_bw20_ch6(self, setUp):
        """Test bandwidth 20/channel 6 in 2.4Ghz interface"""

        self.common_channel(band='20', channel='6')