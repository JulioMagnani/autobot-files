from channel_parent import Channel

class TestBw40Ch2(Channel):

    def test_bw40_ch2(self, setUp):
        """Test bandwidth 40/channel 2 in 2.4Ghz interface"""

        self.common_channel(band='40', channel='2')