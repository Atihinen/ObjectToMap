from lib.db import Base
from sqlalchemy import Column, Integer, Sequence, String
from utils import validator

class FireHydrant(Base):
    __tablename__ = 'fire_hydrant'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    name = Column(String(50))
    description = Column(String(50))
    trunk_line_diameter = Column(String(50))


    def __init__(self, name=None):
        if name:
            self.validate_name(name)


    def validate_name(self, name):
        if name:
            if len(name) > 50:
                raise ValueError("Name can only be 50 characters, name was {} long".format(len(name)))
            self.name = name
        else:
            raise  ValueError("Name cannot be empty")

    def validate_number(self, val):
        if val:
            try:
                val = float(val)
                return True, val
            except ValueError:
                return False, "INVALID_VALUE"
        return False, "NONE_OBJECT"

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name
        self.errors = {}

    def validate_name(self):
        is_empty = validator.validate_empty(self.name)
        if is_empty:
            self.errors["name": "Cannot be empty"]
        is_not_valid = validator.validate_length(self.name, 50)
        if is_not_valid:
            self.errors["name": "Was too long"]

    def validate(self):
        return self.errors
