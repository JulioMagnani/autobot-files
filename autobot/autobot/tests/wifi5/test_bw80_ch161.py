from channel_parent import *

class Bw80Ch157(Channel):

    def __init__(self):
        pass

    def test_bw80_ch161(self):
        """Connect client to bandwidth 80/channel 161 5.0Ghz SSID"""

        self.__test_channel(band='80', channel='161/80')