from channel_parent import *

class Bw20Ch9(Channel):

    def __init__(self):
        pass

    def test_bw20_ch9(self):
        """Test bandwidth 20/channel 9 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='9')