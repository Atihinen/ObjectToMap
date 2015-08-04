__author__ = 'jjauhiainen'
import unittest2 as unittest
from utils import validator

class TestValidator(unittest.TestCase):

    def test_validate_empty(self):
        self.assertEqual(validator.validate_empty(""),
                         validator.ErrorMessages.EMPTY_VAL)
        self.assertEqual(validator.validate_empty("not empty"),
                         validator.ErrorMessages.OK)

    def test_validate_length(self):
        self.assertEqual(validator.validate_length("asd", 1),
                         validator.ErrorMessages.TOO_LONG)
        self.assertEqual(validator.validate_length("asd",3),
                         validator.ErrorMessages.OK)
        self.assertEqual(validator.validate_length("123", 4),
                         validator.ErrorMessages.OK)

    def test_validate_integer(self):
        self.assertEqual(validator.validate_integer(123),
                         validator.ErrorMessages.OK)
        self.assertEqual(validator.validate_integer("1231"),
                         validator.ErrorMessages.OK)
        self.assertEqual(validator.validate_integer("asdsa"),
                         validator.ErrorMessages.NOT_NUMBER)
        self.assertEqual(validator.validate_integer("123,12"),
                         validator.ErrorMessages.NOT_NUMBER)
        self.assertEqual(validator.validate_integer("123.10"),
                         validator.ErrorMessages.NOT_NUMBER)

    def test_validate_float(self):
        self.assertEqual(validator.validate_float(123),
                         validator.ErrorMessages.OK)
        self.assertEqual(validator.validate_float("123"),
                         validator.ErrorMessages.OK)
        self.assertEqual(validator.validate_float(123.1),
                         validator.ErrorMessages.OK)
        self.assertEqual(validator.validate_float("0.12"),
                         validator.ErrorMessages.OK)
        self.assertEqual(validator.validate_float("asd"),
                         validator.ErrorMessages.NOT_NUMBER)
        self.assertEqual(validator.validate_float("1232,12"),
                         validator.ErrorMessages.NOT_NUMBER)

