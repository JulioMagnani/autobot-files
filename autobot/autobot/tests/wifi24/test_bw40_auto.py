from channel_parent import Channel

class TestBw40Auto(Channel):

    def test_bw40_auto(self, setUp):
        """Test bandwidth 40/channel auto in 2.4Ghz interface"""

        self.common_channel(band='40', channel='0')