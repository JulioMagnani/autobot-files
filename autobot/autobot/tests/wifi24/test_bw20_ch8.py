from channel_parent import *

class Bw20Ch8(Channel):

    def __init__(self):
        pass

    def test_bw20_ch8(self):
        """Test bandwidth 20/channel 8 in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='8')