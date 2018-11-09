from bandwidth_parent import *

class Bandwidth20(Bandwidth):

    def __init__(self):
        pass

    def test_bw_20(self):
        """20MHz bandwidth connectivity from a client to the DUT"""

        self.__test_bandwidth(band='20')