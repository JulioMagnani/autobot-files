class Error(Exception):
    """Base class for exceptions"""
    pass


class SeleniumServerError(Error):
    """Exception raised for selenium server errors

    Attributes:
        expression -- where the error occurred
        message -- explanation of the error
    """

    def __init__(self, exp, msg):
        self.expression = exp
        self.message = msg


class NetworkError(Error):
    """Exception raised for Network Operation errors

    Attributes:
        expression -- where the error occurred
        message -- explanation of the error
    """

    def __init__(self, exp, msg):
        self.expression = exp
        self.message = msg


class WifiConnError(Error):
    """Exception raised for errors in wifi connection

    Attributes:
        expression -- where the error occurred
        message -- explanation of the error
    """

    def __init__(self, exp, msg):
        self.expression = exp
        self.message = msg


class WebElementError(Error):
    """Exception raised for errors in selenium webdriver

    Attributes:
        expression -- where the error occurred
        message -- explanation of the error
    """

    def __init__(self, element, message):
        self.element = element
        self.message = message


class ElementMatchError(Error):
    """Exception raised for errors in selenium webdriver

    Attributes:
        expression -- where the error occurred
        message -- explanation of the error
    """

    def __init__(self, element_1, element_2, message):
        self.element_1 = element_1
        self.element_2 = element_2
        self.message = message


class ElementError(Error):
    """Exception raised for errors in selenium webdriver

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
