from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from autobot.PageObjects.locators import (LoginLocators, RadioLocators,
                                          NetworkLocators, SoftwareLocators,
                                          MacFilterLocators)


class BasePage:

    def __init__(self, webdriver):
        self.driver = webdriver

    def refresh_page(self):
        self.driver.refresh()
        self.driver.implicitly_wait(30)

    def GO_TO(self, url=None):
        return self.driver.get(url)

    def enable(self, sel_elem):
        """Choose enable option in a dropdown menu

        :Args:
         - sel_elem: a selenium obj containing a dropdown menu
        """

        enable = "option[value*='1']"
        sel_elem.find_element(By.CSS_SELECTOR, enable).click()

    def disable(self, sel_elem):
        """Disable a selenium web element passed as param"""

        disable = "option[value*='0']"
        sel_elem.find_element(By.CSS_SELECTOR, disable).click()

    def is_enabled(self, sel_elem):
        """Check if a selenium web obj passed as param is enabled"""

        selected = "option[selected='']"
        enabled = sel_elem.find_element(By.CSS_SELECTOR, selected)
        if enabled.text == "Enabled":
            return True

        return False

    def is_title(self):
        """Get str title of current page"""

        return self.driver.title

    def apply_changes(self):
        pass


class LoginPage(BasePage):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.driver.get('http://192.168.0.1/')

    def enter_credentials(self, username, password):
        USERNAME = self.driver.find_element(*LoginLocators.USERNAME)
        PASSWORD = self.driver.find_element(*LoginLocators.PASSWORD)
        APPLY_BTN = self.driver.find_element(*LoginLocators.APPLY_BTN)

        USERNAME.send_keys(username)
        PASSWORD.send_keys(password)
        APPLY_BTN.click()


class RadioPage(BasePage):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.driver.get('http://192.168.0.1/wlanRadio.asp')

    def select_wifi_interface(self, iface=None):
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
        APPLY_BTN = self.driver.find_element(*RadioLocators.APPLY_BTN)
        APPLY_BTN.click()

        self.refresh_page()

    def reset_wireless_default(self):
        RESET_BTN = self.driver.find_element(*RadioLocators.RESET_BTN)
        RESET_BTN.click()

        self.refresh_page()


class NetworkPage(BasePage):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.driver.get('http://192.168.0.1/wlanPrimaryNetwork.asp')

    def get_wpa(self):
        return self.driver.find_element(*NetworkLocators.WPA)

    def get_wpa2(self):
        return self.driver.find_element(*NetworkLocators.WPA_2)

    def get_primary_network(self):
        return self.driver.find_element(*NetworkLocators.PRIMARY_NETWORK)

    def set_ssid_name(self, name):
        SSID = self.__get_ssid()
        SSID.clear()
        SSID.send_keys(name)

    def get_ssid_name(self):
        return self.__get_ssid().get_attribute('value')

    def enable_wpa2(self):
        WPA_2 = self.driver.find_element(*NetworkLocators.WPA_2)

        enable = "option[value*='1']"
        enable_wpa2 = WPA_2.find_element(By.CSS_SELECTOR, enable)
        enable_wpa2.click()

    def wpa_is_selected(self):
        WPA = self.driver.find_element(*NetworkLocators.WPA)

        return self.__is_enabled(WPA)

    def wpa2_is_selected(self):
        WPA_2 = self.driver.find_element(*NetworkLocators.WPA_2)

        return self.__is_enabled(WPA_2)

    def enable_wpa(self):
        WPA = self.driver.find_element(*NetworkLocators.WPA)

        enable = "option[value*='1']"
        enable_wpa = WPA.find_element(By.CSS_SELECTOR, enable)
        enable_wpa.click()

    def enable_network(self):
        NETWORK = self.driver.find_element(*NetworkLocators.PRIMARY_NETWORK)

        self.__enable_element(NETWORK)

    def is_network_enabled(self):
        NETWORK = self.driver.find_element(*NetworkLocators.PRIMARY_NETWORK)

        return self.__is_enabled(NETWORK)

    def set_encryption(self, crypt):
        ENCRYPTION = self.driver.find_element(*NetworkLocators.ENCRYPTION)

        options = ENCRYPTION.find_elements(By.TAG_NAME, "option")
        for option in options:
            if crypt in option.text:
                option.click()
                break
        return None

    def get_encryption(self):
        ENCRYPTION = self.driver.find_element(*NetworkLocators.ENCRYPTION)

        options = ENCRYPTION.find_elements(By.TAG_NAME, "option")
        for option in options:
            if option.get_attribute("selected"):
                return option.text
        return None

    def set_password(self, password):
        PASSWORD = self.driver.find_element(*NetworkLocators.PASSWORD)

        PASSWORD.clear()
        PASSWORD.send_keys(password)

    def get_password(self):
        PASSWORD = self.driver.find_element(*NetworkLocators.PASSWORD)

        return PASSWORD.get_attribute('value')

    def apply_changes(self):
        APPLY_BTN = self.driver.find_element(*NetworkLocators.APPLY_BTN)
        APPLY_BTN.click()

        self.__accept_alert()  # handle alert popup
        self.refresh_page()

    def __enable_element(self, element):

        enable = "option[value*='1']"
        enable_el = element.find_element(By.CSS_SELECTOR, enable)
        enable_el.click()

    def __accept_alert(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                                'wait for confirmation alert')
            self.driver.switch_to.alert.accept()
        except Exception:
            pass

    def __get_ssid(self):
        return self.driver.find_element(*NetworkLocators.SSID)


class SoftwarePage(BasePage):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.driver.get('http://192.168.0.1/RgSwInfo.asp')

    def get_serial_number(self):
        return self.driver.find_element(*SoftwareLocators.SERIAL_NUMBER).text


class ConnectionPage(BasePage):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.driver.get('http://192.168.0.1/RgConnect.asp')


class AdvancedPage(BasePage):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.driver.get('http://192.168.0.1/RgMacFiltering.asp')

    def set_mac_address(self, adrr):
        """Set mac address in Web UI Advanced Page"""
        MAC_ADDRESS = self.__mac_addr()

        MAC_ADDRESS.clear()
        MAC_ADDRESS.send_keys(adrr)

    def check_error_page(self):
        return self.__error_window()

    def click_add_btn(self):
        self.__add_mac_btn().click()
        self.refresh_page()

    def click_clear_all_btn(self):
        self.__clear_all_btn().click()
        self.refresh_page()

    def __mac_addr(self):
        return self.driver.find_element(*MacFilterLocators.MAC_ADDRESS)

    def __add_mac_btn(self):
        return self.driver.find_element(*MacFilterLocators.ADD_MAC_BTN)

    def __clear_all_btn(self):
        return self.driver.find_element(*MacFilterLocators.RM_ALL_BTN)

    def __error_link(self):
        return self.driver.find_element(*MacFilterLocators.ERROR_LINK)

    def __error_window(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.alert_is_present(), 'waiting for alert message')

            alert = self.driver.switch_to.alert
            alert.accept()
            return True
        except Exception:
            return False
