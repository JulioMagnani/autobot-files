from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from autobot.PageObjects.pages import BasePage
from autobot.PageObjects.locators import RadioLocators


class RadioPage(BasePage):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.driver.get('http://192.168.0.1/wlanRadio.asp')

    def select_wifi_interface(self, iface=None):
        """@deprecated"""

        if iface == '2.4GHZ':
            WIFI_IFACE = self.driver.find_element(*RadioLocators.WIFI_24_IFACE)
        elif iface == '5.0GHZ':
            WIFI_IFACE = self.driver.find_element(*RadioLocators.WIFI_5_IFACE)

        WIFI_IFACE.click()

    def get_wireless(self):
        return self.driver.find_element(*RadioLocators.WIRELESS)

    def select_bandwidth(self, bandwidth):
        BAND_MENU = self.driver.find_element(*RadioLocators.BAND_MENU)

        select_band = "option[value*='{0}']".format(bandwidth)
        band_option = BAND_MENU.find_element_by_css_selector(select_band)
        band_option.click()

    def get_n_mode(self):
        return self.driver.find_element(*RadioLocators.N_MODE)

    def is_nmode_enabled(self):
        N_MODE = self.get_n_mode()

        selected = "option[selected='']"
        enabled = N_MODE.find_element(By.CSS_SELECTOR, selected)
        if enabled.text == "Auto":
            return True

        return False

    def get_wifi_interface(self):
        WIFI_IFACE = self.driver.find_element(*RadioLocators.WIFI_INTERFACE)

        return WIFI_IFACE.text

    def get_bandwidth(self):
        BAND_MENU = self.driver.find_element(*RadioLocators.BAND_MENU)

        selected = "option[selected='']"
        active_band = BAND_MENU.find_element(By.CSS_SELECTOR, selected)
        return active_band.get_attribute('value')

    def set_channel(self, channel):
        CHANNEL_MENU = self.driver.find_element(*RadioLocators.CHANNEL_MENU)

        channel_path = "option[value*='{0}']".format(channel)
        channel = CHANNEL_MENU.find_element(By.CSS_SELECTOR, channel_path)
        channel.click()

    def get_channel(self):
        CHANNEL_MENU = self.driver.find_element(*RadioLocators.CHANNEL_MENU)

        selected = "option[selected='']"
        channel = CHANNEL_MENU.find_element(By.CSS_SELECTOR, selected)
        return channel.get_attribute('value')

    def enable_wireless(self):
        WIFI_ENABLE = self.driver.find_element(*RadioLocators.WIFI_ENABLE)
        WIFI_ENABLE.click()

    def wireless_isenabled(self):
        WIFI_MENU = self.driver.find_element(*RadioLocators.WIFI_SELECTED)
        return WIFI_MENU.text

    def apply_changes(self):
        self.__get_apply_btn().click()
        self.refresh_page()

    def reset_wireless_default(self):
        self.__get_reset_btn().click()

    def click_on_scan(self):
        self.__get_scan_btn().click()

    def __get_apply_btn(self):
        return self.driver.find_element(*RadioLocators.APPLY_BTN)

    def __get_reset_btn(self):
        return self.driver.find_element(*RadioLocators.RESET_BTN)

    def __get_scan_btn(self):
        scan_btn = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(RadioLocators.SCAN_BTN))
        return scan_btn
