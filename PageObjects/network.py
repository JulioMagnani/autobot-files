from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PageObjects.pages import BasePage
from PageObjects.locators import NetworkLocators


class NetworkPage(BasePage):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.driver.get('http://192.168.0.1/wlanPrimaryNetwork.asp')

    def get_wpa(self):
        return self.driver.find_element(*NetworkLocators.WPA)

    def get_wpa2(self):
        return self.driver.find_element(*NetworkLocators.WPA_2)

    def get_wps(self):
        return self.driver.find_element(*NetworkLocators.WPS)

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
            self.driver.find_element(By.TAG_NAME, 'a').click()
        except Exception:
            pass
        finally:
            self.GO_TO(url='http://192.168.0.1/wlanPrimaryNetwork.asp')

    def __get_ssid(self):
        return self.driver.find_element(*NetworkLocators.SSID)
