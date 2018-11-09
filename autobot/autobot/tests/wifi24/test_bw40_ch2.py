from channel_parent import *

class Bw40Ch2(Channel):

    def __init__(self):
        pass

    def test_bw40_ch2(self):
        """Test bandwidth 40/channel 2 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='2')