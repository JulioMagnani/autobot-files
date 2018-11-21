from channel_parent import *

class Bw20Ch7(Channel):

    def __init__(self):
        pass

    def test_bw20_ch7(self):
        """Test bandwidth 20/channel 7 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='7')