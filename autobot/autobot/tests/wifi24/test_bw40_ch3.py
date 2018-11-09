from channel_parent import *

class Bw40Ch3(Channel):

    def __init__(self):
        pass

    def test_bw40_ch3(self):
        """Test bandwidth 40/channel 3 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='3')