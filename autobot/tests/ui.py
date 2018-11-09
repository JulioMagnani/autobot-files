import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from autobot.assertion import Assert
from autobot.exceptions import SeleniumServerError
from autobot.PageObjects import (security, software, connection, login,
                                 diagnostics, bridge, setup, dhcp, backup,
                                 ipfilter, macfilter, portfilter, forwarding,
                                 portTrigger, dmz, basic, filtering, localLog,
                                 remoteLog, radio, network, bridging)


class TestUI(unittest.TestCase):
    """
       Check webUi pages are online and accessible from browsers
       (firefox and chrome)
    """

    USERNAME = None
    PASSWORD = None

    @classmethod
    def setUpClass(cls):

        try:
            cls.firefox = webdriver.Remote(
                desired_capabilities=DesiredCapabilities.FIREFOX)
        except Exception:
            raise SeleniumServerError(
                'Remote webdriver',
                'Could not reach selenium servers. Check docker!')

        login_page = login.LoginPage(cls.firefox)
        login_page.enter_credentials(cls.USERNAME, cls.PASSWORD)

        try:
            cls.chrome = webdriver.Remote(
                desired_capabilities=DesiredCapabilities.CHROME)
        except Exception:
            raise SeleniumServerError(
                'Remote webdriver',
                'Could not reach selenium servers. Check docker!')

        login_page = login.LoginPage(cls.chrome)
        login_page.enter_credentials(cls.USERNAME, cls.PASSWORD)

    @classmethod
    def tearDownClass(cls):
        cls.firefox.quit()
        cls.chrome.quit()

    def suite(self, selected_tests):
        tests = selected_tests

        return unittest.TestSuite(map(TestUI, tests))

    @classmethod
    def set_login(cls, login_info):
        cls.USERNAME = login_info['username']
        cls.PASSWORD = login_info['password']

    def test_statusPage_ff(self):
        """ Check status page tabs are online on firefox"""

        soft_page = software.SoftwarePage(self.firefox)
        assert 'Software' in soft_page.is_title()

        conn_page = connection.ConnectionPage(self.firefox)
        assert 'Connection' in conn_page.is_title()

        sec_page = security.SecurityPage(self.firefox)
        assert 'Security' in sec_page.is_title()

        diag_page = diagnostics.DiagnosticsPage(self.firefox)
        assert 'Diagnostics' in diag_page.is_title()

        bridge_page = bridge.BridgePage(self.firefox)
        assert 'Bridge Mode' in bridge_page.is_title()

    def test_basicPage_ff(self):
        """ Check basic page tabs are online on firefox"""

        setup_page = setup.SetupPage(self.firefox)
        assert 'Basic' in setup_page.is_title()

        dhcp_page = dhcp.DhcpPage(self.firefox)
        assert 'DHCP' in dhcp_page.is_title()

        backup_page = backup.BackupPage(self.firefox)
        assert 'Backup' in backup_page.is_title()

    def test_advPage_ff(self):
        """ Check all advanced page tabs are online on firefox"""

        ipfilt_page = ipfilter.IpFilterPage(self.firefox)
        assert 'IP Filtering' in ipfilt_page.is_title()

        macfilt_page = macfilter.MacFilterPage(self.firefox)
        assert 'MAC Filtering' in macfilt_page.is_title()

        portfilt_page = portfilter.PortFilterPage(self.firefox)
        assert 'Port Filtering' in portfilt_page.is_title()

        forward_page = forwarding.ForwardingPage(self.firefox)
        assert 'Forwarding' in forward_page.is_title()

        pTrigger_page = portTrigger.PortTriggerPage(self.firefox)
        assert 'Port Triggers' in pTrigger_page.is_title()

        dmz_page = dmz.DmzPage(self.firefox)
        assert 'DMZ Host' in dmz_page.is_title()

    def test_firewallPage_ff(self):
        """ Check all firewall page tabs are online on firefox"""

        basic_page = basic.BasicPage(self.firefox)
        assert 'Web Content Filter' in basic_page.is_title()

        filtering_page = filtering.FilteringPage(self.firefox)
        assert 'Filtering' in filtering_page.is_title()

        local_log_page = localLog.LocalLogPage(self.firefox)
        assert 'Local Log' in local_log_page.is_title()

        remote_log_page = remoteLog.RemoteLogPage(self.firefox)
        assert 'Remote Log' in remote_log_page.is_title()

    def test_wirelessPage_ff(self):
        """ Check all wireless page tabs are online on firefox"""

        radio_page = radio.RadioPage(self.firefox)
        assert 'Radio' in radio_page.is_title()

        netwrk_page = network.NetworkPage(self.firefox)
        assert 'Primary Network' in netwrk_page.is_title()

        bridging_page = bridging.BridgingPage(self.firefox)
        assert 'Bridging' in bridging_page.is_title()

    def test_statusPage_chr(self):
        """ Check status page tabs are online on chrome"""

        soft_page = software.SoftwarePage(self.chrome)
        assert 'Software' in soft_page.is_title()

        conn_page = connection.ConnectionPage(self.chrome)
        assert 'Connection' in conn_page.is_title()

        sec_page = security.SecurityPage(self.chrome)
        assert 'Security' in sec_page.is_title()

        diag_page = diagnostics.DiagnosticsPage(self.chrome)
        assert 'Diagnostics' in diag_page.is_title()

        bridge_page = bridge.BridgePage(self.chrome)
        assert 'Bridge Mode' in bridge_page.is_title()

    def test_basicPage_chr(self):
        """ Check basic page tabs are online on chrome"""

        setup_page = setup.SetupPage(self.chrome)
        assert 'Setup' in setup_page.is_title()

        dhcp_page = dhcp.DhcpPage(self.chrome)
        assert 'DHCP' in dhcp_page.is_title()

        backup_page = backup.BackupPage(self.chrome)
        assert 'Backup' in backup_page.is_title()

    def test_advPage_chr(self):
        """ Check all advanced page tabs are online on chrome"""

        ipfilt_page = ipfilter.IpFilterPage(self.chrome)
        assert 'IP Filtering' in ipfilt_page.is_title()

        macfilt_page = macfilter.MacFilterPage(self.chrome)
        assert 'MAC Filtering' in macfilt_page.is_title()

        portfilt_page = portfilter.PortFilterPage(self.chrome)
        assert 'Port Filtering' in portfilt_page.is_title()

        forward_page = forwarding.ForwardingPage(self.chrome)
        assert 'Forwarding' in forward_page.is_title()

        pTrigger_page = portTrigger.PortTriggerPage(self.chrome)
        assert 'Port Triggers' in pTrigger_page.is_title()

        dmz_page = dmz.DmzPage(self.chrome)
        assert 'DMZ Host' in dmz_page.is_title()

    def test_firewallPage_chr(self):
        """ Check all firewall page tabs are online on chrome"""

        basic_page = basic.BasicPage(self.chrome)
        assert 'Web Content Filter' in basic_page.is_title()

        filtering_page = filtering.FilteringPage(self.chrome)
        assert 'Filtering' in filtering_page.is_title()

        local_log_page = localLog.LocalLogPage(self.chrome)
        assert 'Local Log' in local_log_page.is_title()

        remote_log_page = remoteLog.RemoteLogPage(self.chrome)
        assert 'Remote Log' in remote_log_page.is_title()

    def test_wirelessPage_chr(self):
        """ Check all wireless page tabs are online on chrome"""

        radio_page = radio.RadioPage(self.chrome)
        assert 'Radio' in radio_page.is_title()

        netwrk_page = network.NetworkPage(self.chrome)
        assert 'Primary Network' in netwrk_page.is_title()

        bridging_page = bridging.BridgingPage(self.chrome)
        assert 'Bridging' in bridging_page.is_title()

    def test_mac_filter_blank(self):
        """MAC filtering - blank space as mac addr"""

        assertion = Assert()

        # Go to page Advanced
        macfilter_page = macfilter.MacFilterPage(self.firefox)

        # Add a blank mac on field
        mac_address = ' '
        macfilter_page.set_mac_address(mac_address)
        macfilter_page.click_add_btn()

        # Assert error message
        try:
            assertion.is_true(macfilter_page.check_error_page(),
                              'error window')
        finally:
            # remove mac filter added
            macfilter_page = macfilter.MacFilterPage(self.firefox)
            macfilter_page.click_clear_all_btn()

    def test_mac_filter_invalid(self):
        """MAC filtering - invalid space as mac addr"""

        assertion = Assert()

        # Go to page Advanced
        macfilter_page = macfilter.MacFilterPage(self.firefox)

        # Add a invalid mac field
        mac_address = '88:88:88:88:88:GG'
        macfilter_page.set_mac_address(mac_address)
        macfilter_page.click_add_btn()

        # Assert error message
        try:
            assertion.is_true(macfilter_page.check_error_page(),
                              'error window')
        finally:
            # remove mac filter added
            macfilter_page = macfilter.MacFilterPage(self.firefox)
            macfilter_page.click_clear_all_btn()
