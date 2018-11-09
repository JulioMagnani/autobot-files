from channel_parent import *

class Bw20Auto(Channel):

    def __init__(self):
        pass

    def test_bw20_auto(self):
        """Test bandwidth 20/channel auto in 2.4Ghz interface"""

        self.__test_channel(band='20', channel='0')