from selenium.webdriver.common.by import By


class LoginLocators:

    USERNAME = (By.NAME, 'loginUsername')
    PASSWORD = (By.NAME, 'loginPassword')
    APPLY_BTN = (By.CSS_SELECTOR,
                 'tbody>tr:nth-child(3)>td>input[type=submit]')


class SecurityLocators:

    RESET_FAC_YES = (By.NAME, 'RestoreFactoryYes')
    APPLY_BTN = (By.CSS_SELECTOR, "input[value*='Apply']")


class RadioLocators:

    WIFI_INTERFACE = (By.NAME, "Band")
    WIRELESS = (By.NAME, "WirelessEnable")
    WIFI_24_IFACE = (By.CSS_SELECTOR,
                     "select[name*='WirelessMacAddress']>option[value*='1']")

    WIFI_5_IFACE = (By.CSS_SELECTOR,
                    "select[name*='WirelessMacAddress']>option[value*='0']")

    WIFI_ENABLE = (By.CSS_SELECTOR,
                   "select[name*='WirelessEnable']>option[value*='1']")

    WIFI_DISABLE = (By.CSS_SELECTOR,
                    "select[name*='WirelessEnable']>option[value*='0']")

    WIFI_SELECTED = (By.CSS_SELECTOR,
                     "select[name*='WirelessEnable']>option[selected='']")

    BAND_MENU = (By.NAME, 'NBandwidth')
    N_MODE = (By.NAME, 'NMode')
    CHANNEL_MENU = (By.NAME, "ChannelNumber")
    APPLY_BTN = (By.CSS_SELECTOR, "input[onclick*='commitRadio()']")
    RESET_BTN = (By.CSS_SELECTOR, "input[value*='Restore Wireless Defaults']")
    SCAN_BTN = (By.CSS_SELECTOR, "input[value*='Scan Wireless APs']")


class NetworkLocators:

    PRIMARY_NETWORK = (By.NAME, 'PrimaryNetworkEnable')
    SSID = (By.NAME, 'ServiceSetIdentifier')
    WPA_2 = (By.NAME, 'Wpa2PskAuth')
    WPA = (By.NAME, 'WpaPskAuth')
    WPS = (By.NAME, 'AutoSecurity')
    ENCRYPTION = (By.NAME, 'WpaEncryption')
    SHOW_PASS_CHECKBOX = (By.NAME, 'ShowWpaKey')
    PASSWORD = (By.NAME, 'WpaPreSharedKey')
    APPLY_BTN = (By.CSS_SELECTOR, "input[value*='Apply']")


class SoftwareLocators:

    SERIAL_NUMBER = (By.CSS_SELECTOR,
                     "table>tbody>tr:nth-child(6)>td:nth-child(2)")


class MacFilterLocators:

    MAC_ADDRESS = (By.NAME, 'NewMacFilter')
    ADD_MAC_BTN = (By.CSS_SELECTOR, "input[onclick*='AddMacFilter()']")
    RM_ALL_BTN = (By.CSS_SELECTOR, "input[onclick*='ClearAllMac()']")
    ERROR_LINK = (By.LINK_TEXT, 'TRY AGAIN')


class BasicLocators:

    LOCAL_IPV6 = (By.CSS_SELECTOR, "table>tbody>tr:nth-child(30)>td:nth-child(3)")
