from bandwidth_parent import Bandwidth

class TestBandwidth40(Bandwidth):

    def test_bw_40(self, setUp):
        """40MHz bandwidth connectivity from a client to the DUT"""

        self.common_bandwidth(band='40')