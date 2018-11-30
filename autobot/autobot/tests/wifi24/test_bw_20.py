from bandwidth_parent import Bandwidth

class TestBandwidth20(Bandwidth):

    def test_bw_20(self, setUp):
        """20MHz bandwidth connectivity from a client to the DUT"""

        self.common_bandwidth(band='20')