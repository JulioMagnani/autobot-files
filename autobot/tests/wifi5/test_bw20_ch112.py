from channel_parent import *

class Bw20Ch112(Channel):

    def __init__(self):
        pass

    def test_bw20_ch112(self):
        """Connect client to bandwidth 20/channel 112 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='112')