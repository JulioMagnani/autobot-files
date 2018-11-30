from channel_parent import Channel

class TestBw40Ch9(Channel):

    def test_bw40_ch9(self, setUp):
        """Test bandwidth 40/channel 9 in 2.4Ghz interface"""

        self.common_channel(band='40', channel='9')