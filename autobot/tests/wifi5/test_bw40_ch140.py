from channel_parent import *

class Bw40Ch140(Channel):

    def __init__(self):
        pass

    def test_bw40_ch140(self):
        """Connect client to bandwidth 40/channel 140 5.0Ghz SSID"""

        self.__test_channel(band='40', channel='140')