from channel_parent import *

class Bw40Ch4(Channel):

    def __init__(self):
        pass

    def test_bw40_ch4(self):
        """Test bandwidth 40/channel 4 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='4')