from channel_parent import Channel

class TestBw40Ch7(Channel):

    def test_bw40_ch7(self, setUp):
        """Test bandwidth 40/channel 7 in 2.4Ghz interface"""

        self.comon_channel(band='40', channel='7')