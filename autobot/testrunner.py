import os
import unittest
from autobot.tests.loader import Test
from autobot.log import Output
from autobot import reportgenerator
from autobot.tests import ui, dhcp, wifi24, wifi5, ipv6


class TestRunner:
    """
    Create and run unittest based script tests
    """

    def __init__(self, test_list):
        """test_list: str list"""

        self.test_list = test_list

    def load_tests(self, login_info):
        """
        Create a test suite fixture from a string list
        """

        ui_tests = []
        dhcp_tests = []
        wifi24_tests = []
        wifi5_tests = []
        ipv6_tests = []

        # create a str list with each script module name
        if self.test_list:
            for test in self.test_list:
                scripts = Test().get_module(test)
                for script in scripts:
                    suite_desc, test_desc = script.split('.')
                    if suite_desc == 'TestUI':
                        ui_tests.append(test_desc)
                    elif suite_desc == 'TestDHCP':
                        dhcp_tests.append(test_desc)
                    elif suite_desc == 'TestWifi24':
                        wifi24_tests.append(test_desc)
                    elif suite_desc == 'TestWifi5':
                        wifi5_tests.append(test_desc)
                    elif suite_desc == 'TestIpv6':
                        ipv6_tests.append(test_desc)

        # load all suites classes
        ui_ = ui.TestUI()
        dhcp_ = dhcp.TestDHCP()
        wifi_24_ = wifi24.TestWifi24()
        wifi_5_ = wifi5.TestWifi5()
        ipv6_ = ipv6.TestIpv6()

        # pass login information
        ui_.set_login(login_info)
        dhcp_.set_login(login_info)
        wifi_24_.set_login(login_info)
        wifi_5_.set_login(login_info)
        ipv6_.set_login(login_info)

        # load unittest obj for each suite
        allsuites = unittest.TestSuite(
            [
                ui_.suite(ui_tests),
                dhcp_.suite(dhcp_tests),
                wifi_24_.suite(wifi24_tests),
                wifi_5_.suite(wifi5_tests),
                ipv6_.suite(ipv6_tests)
            ])

        return allsuites

    def run_suite(self, suite):
        """
        run test suite and create a folder containing an HTML report
        """

        # configure HTMLTestRunner options
        current_dir = os.getcwd()
        reports_folder = '{0}/reports'.format(current_dir)
        if not os.path.isdir(reports_folder):
            os.makedirs(reports_folder)

        html_runner = reportgenerator.HTMLTestRunner(
            output='TestReports'.format(reports_folder),
            report_title='Test Report', stream=Output())
        try:
            html_runner.run(suite)
        except ConnectionRefusedError:
            print('Cant reach selenium servers')
