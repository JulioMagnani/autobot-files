from channel_parent import *

class Bw40Ch6(Channel):

    def __init__(self):
        pass

    def test_bw40_ch6(self):
        """Test bandwidth 40/channel 6 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='6')