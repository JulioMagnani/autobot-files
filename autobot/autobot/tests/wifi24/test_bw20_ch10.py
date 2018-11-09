from channel_parent import *

class Bw20Ch10(Channel):

    def __init__(self):
        pass

    def test_bw20_ch10(self):
        """Test bandwidth 20/channel 10 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='10')
