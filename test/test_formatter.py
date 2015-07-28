__author__ = 'jjauhiainen'
import unittest2 as unittest
from utils import formatter
from utils.validator import ErrorMessages

class TestFormatter(unittest.TestCase):

    def test_convert_to_integer(self):
        self.assertEqual(3, formatter.convert_to_integer(3))
        self.assertEqual(3, formatter.convert_to_integer("3"))
        self.assertEqual(3, formatter.convert_to_integer(3.4))
        self.assertEqual(ErrorMessages.NOT_NUMBER,
                         formatter.convert_to_integer("asdsd"))
        self.assertEqual(ErrorMessages.NOT_NUMBER,
                         formatter.convert_to_integer("3.4"))
