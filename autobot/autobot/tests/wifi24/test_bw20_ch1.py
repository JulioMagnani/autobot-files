from channel_parent import Channel

class TestBw20Ch1(Channel):

    def test_bw20_ch1(self, setUp):
        """Test bandwidth 20/channel 1 in 2.4Ghz interface"""

        self.common_channel(band='20', channel='1')