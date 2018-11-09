from channel_parent import *

class Bw20Ch11(Channel):

    def __init__(self):
        pass

    def test_bw20_ch11(self):
        """Test bandwidth 20/channel 11 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='11')