from channel_parent import Channel

class TestBw20Auto(Channel):

    def test_bw20_auto(self, setUp):
        """Test bandwidth 20/channel auto in 2.4Ghz interface"""

        self.common_channel(band='20', channel='0')