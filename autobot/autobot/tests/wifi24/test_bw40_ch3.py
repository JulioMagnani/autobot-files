from channel_parent import Channel

class TestBw40Ch3(Channel):

    def test_bw40_ch3(self, setUp):
        """Test bandwidth 40/channel 3 in 2.4Ghz interface"""

        self.common_channel(band='40', channel='3')