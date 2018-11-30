from channel_parent import Channel

class TestBw20Ch5(Channel):

    def test_bw20_ch5(self, setUp):
        """Test bandwidth 20/channel 5 in 2.4Ghz interface"""

        self.common_channel(band='20', channel='5')