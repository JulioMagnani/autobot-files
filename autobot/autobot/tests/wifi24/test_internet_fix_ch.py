from channel_parent import Channel

class TestInternetFixCh(Channel):

    def test_internet_fix_ch(self, setUp):
        """Test internet connection w fixed channel"""

        self.common_channel(band='20', channel='1', url='www.google.com')