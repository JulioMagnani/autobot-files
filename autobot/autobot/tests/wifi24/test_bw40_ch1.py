from channel_parent import Channel

class TestBw40Ch1(Channel):

    def test_bw40_ch1(self, setUp):
        """Test bandwidth 40/channel 1 in 2.4Ghz interface"""

        self.common_channel(band='40', channel='1')