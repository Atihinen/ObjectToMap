import unittest2 as unittest
from models import Entity

class TestEntity(unittest.TestCase):
    def test_name_is_lowecase(self):
        name = "ASD"
        ent = Entity(name)
        self.assertEqual(name.lower(), ent.name)