from channel_parent import *

class Bw80Ch56(Channel):

    def __init__(self):
        pass

    def test_bw80_ch56(self):
        """Connect client to bandwidth 80/channel 56 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='56/80')