from channel_parent import Channel

class TestBw20Ch3(Channel):

    def test_bw20_ch3(self, setUp):
        """Test bandwidth 20/channel 3 in 2.4Ghz interface"""

        self.common_channel(band='20', channel='3')