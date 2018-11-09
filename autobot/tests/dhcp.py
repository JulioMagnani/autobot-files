import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from ddt import ddt, data


@ddt
class TestDHCP(unittest.TestCase):

    USERNAME = None
    PASSWORD = None
    SSID = None
    SSID_PASS = None

    @classmethod
    def setUpClass(cls):
        cls.firefox = webdriver.Remote(
            desired_capabilities=DesiredCapabilities.FIREFOX)

        # navigate to the page
        cls.firefox = webdriver.Remote(
            desired_capabilities=DesiredCapabilities.FIREFOX)
        cls.firefox.get('http://192.168.0.1')
        cls.firefox.find_element_by_name('loginUsername').send_keys(
                                                                  cls.USERNAME)
        cls.firefox.find_element_by_name('loginPassword').send_keys(
                                                                  cls.PASSWORD)
        cls.firefox.find_element_by_css_selector(
                         'tbody>tr:nth-child(3)>td>input[type=submit]').click()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def suite(self, selected_tests):
        tests = selected_tests

        return unittest.TestSuite(map(TestDHCP, tests))

    @classmethod
    def set_login(cls, login_info):
        cls.USERNAME = login_info['username']
        cls.PASSWORD = login_info['password']
        cls.SSID = login_info['ssid_2.4']
        cls.SSID_PASS = login_info['pass_2.4']

    @data(888)
    def test_ip_range(self, value_dump):
        """Test will pass in case the IP could not be set out of RFC1918 range"""

        # Go to page Basic
        self.search_field = self.driver.find_element_by_link_text('Basic')
        self.search_field.click()

        # Insert ip value on field IPv4 Address
        for value in range(0, 4):

            print("value dump: ")
            print(value_dump)

            self.search_field = self.driver.find_element_by_name("LocalIpAddressIP{}".format(value))
            self.search_field.clear()
            if value == 3:
                self.search_field.send_keys('1')
                break
            self.search_field.send_keys(value_dump)

        # Click on the Apply button
        self.btn = self.driver.find_element_by_css_selector("input[onclick*='ApplyRgSetupButton()']")
        self.btn.click()

        # Check the error message
        self.warn_msg = self.driver.find_element_by_tag_name("h1")
        self.text_to_compare = "Error converting one or more entries:"
        self.assertEqual(self.warn_msg.text, self.text_to_compare)


if __name__ == "__main__":
    unittest.main(verbosity=2)
