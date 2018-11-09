from channel_parent import *

class InternetFixCh(Channel):

    def __init__(self):
        pass

    def test_internet_fix_ch(self):
        """Test internet connection w fixed channel"""

        self.__test_channel(band='20', channel='1', url='www.google.com')