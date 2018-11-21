from bandwidth_parent import *

class Bandwidth40(Bandwidth):

    def __init__(self):
        pass

    def test_bw_40(self):
        """40MHz bandwidth connectivity from a client to the DUT"""

        self.__test_bandwidth(band='40')