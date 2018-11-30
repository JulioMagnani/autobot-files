from channel_parent import Channel

class TestBw40Ch5(Channel):

    def test_bw40_ch5(self, setUp):
        """Test bandwidth 40/channel 5 in 2.4Ghz interface"""

        self.common_channel(band='40', channel='5')