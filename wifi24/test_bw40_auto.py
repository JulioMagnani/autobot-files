from channel_parent import *

class Bw40Auto(Channel):

    def __init__(self):
        pass

    def test_bw40_auto(self):
        """Test bandwidth 40/channel auto in 2.4Ghz interface"""

        self.__test_channel(band='40', channel='0')