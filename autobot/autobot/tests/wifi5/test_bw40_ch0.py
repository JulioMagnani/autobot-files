from channel_parent import *

class Bw40Ch0(Channel):

    def __init__(self):
        pass

    def test_bw40_ch0(self):
        """Connect client to bandwidth 40/channel auto 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='0')