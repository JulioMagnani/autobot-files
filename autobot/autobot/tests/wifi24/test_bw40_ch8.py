from channel_parent import Channel

class TestBw40Ch8(Channel):

    def test_bw40_ch8(self, setUp):
        """Test bandwidth 40/channel 8 in 2.4Ghz interface"""

        self.common_channel(band='40', channel='8')