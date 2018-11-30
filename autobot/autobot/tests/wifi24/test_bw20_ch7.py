from channel_parent import Channel

class TestBw20Ch7(Channel):

    def test_bw20_ch7(self, setUp):
        """Test bandwidth 20/channel 7 in 2.4Ghz interface"""

        self.common_channel(band='20', channel='7')