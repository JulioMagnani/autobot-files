from channel_parent import *

class Bw20Ch136(Channel):

    def __init__(self):
        pass

    ef test_bw20_ch136(self):
        """Connect client to bandwidth 20/channel 136 5.0Ghz SSID"""

        self.__test_channel(band='20', channel='136')