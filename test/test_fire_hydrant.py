"""
import unittest2 as unittest
from models import FireHydrant
from random import randint
class TestFireHydrant(unittest.TestCase):

    def setUp(self):
        self.fh = FireHydrant()

    def test_over_50_char_name_should_be_invalid(self):
        name = ""
        for i in range(51):
            name += chr(randint(0, 255))
        self.assertRaises(ValueError, self.fh.validate_name, name)

    def test_latitude_and_longitude_should_be_numeric(self):
        lat = "1233a"
        lon = "asd1233"
        self.assertRaises(ValueError, self.fh.validate_number, lat)
"""