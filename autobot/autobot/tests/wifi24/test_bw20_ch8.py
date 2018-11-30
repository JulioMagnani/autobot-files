from channel_parent import Channel

class TestBw20Ch8(Channel):

    def test_bw20_ch8(self, setUp):
        """Test bandwidth 20/channel 8 in 2.4Ghz interface"""

        self.common_channel(band='20', channel='8')