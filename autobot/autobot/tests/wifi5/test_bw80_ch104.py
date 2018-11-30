from channel_parent import Channel

class TestBw80Ch104(Channel):
    
    def test_bw80_ch104(self, setUp):
        """Connect client to bandwidth 80/channel 104 5.0Ghz SSID"""

        self.common_channel(band='80', channel='104/80')