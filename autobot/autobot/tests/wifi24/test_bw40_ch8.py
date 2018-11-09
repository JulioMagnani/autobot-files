from channel_parent import *

class Bw40Ch8(Channel):

    def __init__(self):
        pass

    def test_bw40_ch8(self):
        """Test bandwidth 40/channel 8 in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='8')