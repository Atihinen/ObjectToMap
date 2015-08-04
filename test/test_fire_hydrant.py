import unittest2 as unittest
from models import FireHydrant, _empty_val, _not_integer, _too_long, _not_float
from random import randint

class TestFireHydrant(unittest.TestCase):

    def test_should_be_valid_with_valid_values(self):
        fh = FireHydrant("name", "description", "trunk_line_diameter", 1, 1.1, 1.2)
        res = fh.validate()
        self.assertEqual({}, res)

    def test_should_return_correct_messages_with_empty_values(self):
        fh = FireHydrant("", "", "", "", "", "")
        res = fh.validate()
        self.assertTrue("name" in res)
        self.assertEqual(_empty_val, res['name'])
        self.assertTrue('description' in res)
        self.assertEqual(_empty_val, res['description'])
        self.assertTrue('trunk_line_diameter' in res)
        self.assertEqual(_empty_val, res['trunk_line_diameter'])
        self.assertTrue('category_id' in res)
        self.assertEqual(_empty_val, res['category_id'])
        self.assertTrue('latitude' in res)
        self.assertEqual(_empty_val, res['latitude'])
        self.assertTrue('longitude' in res)
        self.assertEqual(_empty_val, res['longitude'])

    def test_should_give_correct_messages_with_invalid_values(self):
        val = ""
        for i in range(51):
            val = "{}{}".format(val, chr(i))
        fh = FireHydrant(val, val, val, "asd", "abs", "dod")
        res = fh.validate()
        self.assertTrue("name" in res)
        self.assertEqual(_too_long, res['name'])
        self.assertTrue('description' in res)
        self.assertEqual(_too_long, res['description'])
        self.assertTrue('trunk_line_diameter' in res)
        self.assertEqual(_too_long, res['trunk_line_diameter'])
        self.assertTrue('category_id' in res)
        self.assertEqual(_not_integer, res['category_id'])
        self.assertTrue('latitude' in res)
        self.assertEqual(_not_float, res['latitude'])
        self.assertTrue('longitude' in res)
        self.assertEqual(_not_float, res['longitude'])

    def test_validate_name_should_give_correct_messages(self):
        fh = FireHydrant("name", "description", "trunk_line_diameter", 1, 1.2, 1.3)
        fh.validate_name()
        self.assertFalse("name" in fh.errors)
        val = ""
        for i in range(51):
            val = "{}{}".format(val, chr(i))
        fh.name = val
        fh.validate_name()
        self.assertTrue("name" in fh.errors)
        self.assertEqual(_too_long, fh.errors['name'])
        fh.name = ""
        fh.validate_name()
        self.assertTrue("name" in fh.errors)
        self.assertEqual(_empty_val, fh.errors['name'])

    def test_validate_description_should_give_correct_messages(self):
        fh = FireHydrant("name", "description", "trunk_line_diameter", 1, 1.2, 1.3)
        fh.validate_description()
        self.assertFalse("description" in fh.errors)
        val = ""
        for i in range(51):
            val = "{}{}".format(val, chr(i))
        fh.description = val
        fh.validate_description()
        self.assertTrue("description" in fh.errors)
        self.assertEqual(_too_long, fh.errors['description'])
        fh.description = ""
        fh.validate_description()
        self.assertTrue("description" in fh.errors)
        self.assertEqual(_empty_val, fh.errors['description'])

    def test_validate_trunk_line_diameter_should_give_correct_messages(self):
        fh = FireHydrant("name", "description", "trunk_line_diameter", 1, 1.2, 1.3)
        fh.validate_trunk_line_diameter()
        self.assertFalse("trunk_line_diameter" in fh.errors)
        val = ""
        for i in range(51):
            val = "{}{}".format(val, chr(i))
        fh.trunk_line_diameter = val
        fh.validate_trunk_line_diameter()
        self.assertTrue("trunk_line_diameter" in fh.errors)
        self.assertEqual(_too_long, fh.errors['trunk_line_diameter'])
        fh.trunk_line_diameter = ""
        fh.validate_trunk_line_diameter()
        self.assertTrue("trunk_line_diameter" in fh.errors)
        self.assertEqual(_empty_val, fh.errors['trunk_line_diameter'])

    def test_validate_category_id_should_give_correct_messages(self):
        fh = FireHydrant("name", "description", "trunk_line_diameter", 1, 1.2, 1.3)
        fh.validate_category_id()
        self.assertFalse("category_id" in fh.errors)
        fh.category_id = "asdd"
        fh.validate_category_id()
        self.assertTrue("category_id" in fh.errors)
        self.assertEqual(_not_integer, fh.errors['category_id'])
        fh.category_id = ""
        fh.validate_category_id()
        self.assertTrue("category_id" in fh.errors)
        self.assertEqual(_empty_val, fh.errors['category_id'])

    def test_validate_latitude_give_correct_messages(self):
        fh = FireHydrant("name", "description", "trunk_line_diameter", 1, 1.2, 1.3)
        fh.validate_latitude()
        self.assertFalse("latitude" in fh.errors)
        fh.latitude = "asdd"
        fh.validate_latitude()
        self.assertTrue("latitude" in fh.errors)
        self.assertEqual(_not_float, fh.errors['latitude'])
        fh.latitude = ""
        fh.validate_latitude()
        self.assertTrue("latitude" in fh.errors)
        self.assertEqual(_empty_val, fh.errors['latitude'])

    def test_validate_longitude_give_correct_messages(self):
        fh = FireHydrant("name", "description", "trunk_line_diameter", 1, 1.2, 1.3)
        fh.validate_longitude()
        self.assertFalse("longitude" in fh.errors)
        fh.longitude = "asdd"
        fh.validate_longitude()
        self.assertTrue("longitude" in fh.errors)
        self.assertEqual(_not_float, fh.errors['longitude'])
        fh.longitude = ""
        fh.validate_longitude()
        self.assertTrue("longitude" in fh.errors)
        self.assertEqual(_empty_val, fh.errors['longitude'])


