from channel_parent import Channel

class TestBw40Ch4(Channel):

    def test_bw40_ch4(self, setUp):
        """Test bandwidth 40/channel 4 in 2.4Ghz interface"""

        self.common_channel(band='40', channel='4')