from channel_parent import *

class Bw20Ch6(Channel):

    def __init__(self):
        pass

    def test_bw20_ch6(self):
        """Test bandwidth 20/channel 6 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='6')