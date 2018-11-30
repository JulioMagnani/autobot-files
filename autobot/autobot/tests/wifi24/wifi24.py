import time, sys, os, pytest
from selenium import webdriver

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "{}/{}".format(os.path.pardir,os.path.pardir))))

from network import NetworkOps as conn
from PageObjects.login import LoginPage
from PageObjects.radio import RadioPage

class Wifi24():

    @pytest.fixture()
    def setUp(self):

        self.driver = '/home/arris/Desktop/AutobotGW2/autobot/autobot/tests/wifi24/geckodriver'

        self.USERNAME = 'NET_F30882'
        self.PASSWORD = 'D42C0FF30882'
        self.SSID = 'NET_2GF30882'
        self.SSID_PASS = '0FF30882'

        self.firefox = webdriver.Firefox(executable_path=self.driver)
        login_page = LoginPage(self.firefox)
        login_page.enter_credentials(self.USERNAME, self.PASSWORD)

        yield

        self.firefox.quit() 

    @classmethod    
    def reset_wifisession(cls, driver, ssid):
        conn().delete_wifi_profile(ssid=ssid)

        radio_page = RadioPage(driver)
        radio_page.reset_wireless_default()

        conn().reset_network_mngr()

