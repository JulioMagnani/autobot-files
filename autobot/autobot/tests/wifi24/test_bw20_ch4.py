from channel_parent import *

class Bw20Ch4(Channel):

    def __init__(self):
        pass

    def test_bw20_ch4(self):
        """Test bandwidth 20/channel 4 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='4')