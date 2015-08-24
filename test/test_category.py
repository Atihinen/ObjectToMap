__author__ = 'jjauhiainen'
import unittest2 as unittest
from models import Category, _empty_val, _not_integer, _too_long, _not_float


class TestCategory(unittest.TestCase):
    def test_should_be_valid_with_valid_values(self):
        name = ""
        for i in range(15):
            name = "{}{}".format(name, chr(i))
        cat = Category(name)
        res = cat.validate()
        self.assertFalse(res)
        name = ""
        for i in range(50):
            name = "{}{}".format(name, chr(i))
        cat.name = name
        res = cat.validate()
        self.assertFalse(res)

    def test_should_give_correct_error_messages_with_invalid_values(self):
        cat = Category("")
        res = cat.validate()
        self.assertTrue("name" in res)
        self.assertEquals(_empty_val, res['name'])
        name = ""
        for i in range(51):
            name = "{}{}".format(name, i)
        cat.name = name
        res = cat.validate()
        self.assertTrue("name" in res)
        self.assertEquals(_too_long, res['name'])

    def test_validate_name(self):
        cat = Category("")
        cat.validate_name()
        self.assertTrue("name" in cat.errors)
        self.assertEquals(_empty_val, cat.errors['name'])
        name = ""
        for i in range(53):
            name = "{}{}".format(name, i)
        cat.name = name
        cat.validate_name()
        self.assertTrue("name" in cat.errors)
        self.assertEquals(_too_long, cat.errors['name'])
