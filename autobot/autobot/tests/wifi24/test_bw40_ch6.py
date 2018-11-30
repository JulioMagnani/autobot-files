from channel_parent import Channel

class TestBw40Ch6(Channel):

    def test_bw40_ch6(self, setUp):
        """Test bandwidth 40/channel 6 in 2.4Ghz interface"""

        self.common_channel(band='40', channel='6')