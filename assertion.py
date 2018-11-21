import unittest
from autobot.exceptions import (NetworkError, WifiConnError, WebElementError,
                                ElementError, ElementMatchError)


class Assert(unittest.TestCase):

    def is_wificonnected(self, connection):
        """check if wifi connection was succesful"""

        try:
            self.assertTrue(connection)
        except AssertionError:
            raise WifiConnError(connection,
                                'Wifi connection attempt unsuccessful!')

    def is_sucessful(self, connection, message):
        """Check if operation was sucessful"""

        try:
            self.assertTrue(connection)
        except AssertionError:
            raise NetworkError(message,
                               'was not sucessful')

    def is_unsucessful(self, connection, message):
        """Check if operation was unsucessful"""

        try:
            self.assertFalse(connection)
        except AssertionError:
            raise NetworkError(message,
                               'was sucessful')

    def is_true(self, exp, message):
        """Check if expression is true"""

        try:
            self.assertTrue(exp)
        except (AssertionError, TypeError):
            raise WebElementError(
                message, 'Element in WebUI doesnt match expected result!')

    def is_false(self, exp, element):
        """Check if an expression is false"""

        try:
            self.assertFalse(exp)
        except (AssertionError, TypeError):
            raise ElementError(
                '{0} is true but should be false'.format(element))

    def is_equal(self, el_1, el_2):
        """Check if two elements are equal"""

        try:
            self.assertEqual(el_1, el_2)
        except AssertionError:
            raise WebElementError(
                el_2, 'Element in WebUI doesnt match expected result!')

    def not_equal(self, el_1, el_2):
        """check if element 1 is different from element 2"""

        try:
            self.assertNotEqual(el_1, el_2)
        except (AssertionError, TypeError):
            raise ElementMatchError(
                '{0} is equal to {1}'.format(el_1, el_2))
