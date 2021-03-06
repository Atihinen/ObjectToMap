# -*- coding: utf-8 -*-
from lib.db import Base, engine, db
from sqlalchemy import Column, Integer, Sequence, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from utils import validator
import json

_empty_val = "EMPTY_VAL"
_too_long = "TOO_LONG"
_not_integer = "NOT_INTEGER"
_not_float = "NOT_FLOAT"
_not_existing = "NOT_EXISTING"

class FireHydrant(Base):
    __tablename__ = 'fire_hydrants'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    description = Column(String(50))
    trunk_line_diameter = Column(String(50))
    latitude = Column(Float)
    longitude = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'))

    def __init__(self, description, trunk_line_diameter, category_id, latitude, longitude):
        self.errors = {}
        self.description = description
        self.trunk_line_diameter = trunk_line_diameter
        self.category_id = category_id
        self.latitude = latitude
        self.longitude = longitude

    def validate_description(self):
        is_not_valid = validator.validate_length(self.description, 50)
        if is_not_valid == validator.ErrorMessages.TOO_LONG:
            self.errors['description'] = _too_long

    def validate_trunk_line_diameter(self):
        is_not_valid = validator.validate_length(self.trunk_line_diameter, 50)
        if is_not_valid == validator.ErrorMessages.TOO_LONG:
            self.errors['trunk_line_diameter'] = _too_long

    def validate_category_id(self):
        is_empty = validator.validate_empty(self.category_id)
        if is_empty == validator.ErrorMessages.EMPTY_VAL:
            self.errors['category_id'] = _empty_val
            return
        is_not_valid = validator.validate_integer(self.category_id)
        if is_not_valid == validator.ErrorMessages.NOT_NUMBER:
            self.errors['category_id'] = _not_integer
            return
        cat = db.query(Category).get(self.category_id)
        if not cat:
            self.errors['category_id'] = _not_existing

    def validate_latitude(self):
        is_empty = validator.validate_empty(self.latitude)
        if is_empty == validator.ErrorMessages.EMPTY_VAL:
            self.errors['latitude'] = _empty_val
            return
        is_not_valid = validator.validate_float(self.latitude)
        if is_not_valid == validator.ErrorMessages.NOT_NUMBER:
            self.errors['latitude'] = _not_float

    def validate_longitude(self):
        is_empty = validator.validate_empty(self.longitude)
        if is_empty == validator.ErrorMessages.EMPTY_VAL:
            self.errors['longitude'] = _empty_val
            return
        is_not_valid = validator.validate_float(self.longitude)
        if is_not_valid == validator.ErrorMessages.NOT_NUMBER:
            self.errors['longitude'] = _not_float

    def validate(self):
        self.errors = {}
        self.validate_description()
        self.validate_trunk_line_diameter()
        self.validate_category_id()
        self.validate_latitude()
        self.validate_longitude()
        return self.errors

    def get_data(self):
        cat = db.query(Category).get(self.category_id)
        d = {
            "id": self.id,
            "category": cat.get_data(),
            "latitude": self.latitude,
            "longitude": self.longitude,
            "description": self.description,
            "trunk_line_diameter": self.trunk_line_diameter
        }
        return d

    def to_json(self):
        return json.dumps(self.get_data())

    def get_category_name(self):
        cat = db.query(Category).get(self.category_id)
        return cat.name

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    name = Column(String(50))
    fire_hydrants = relationship("FireHydrant")

    def __init__(self, name):
        self.name = name
        self.errors = {}

    def validate_name(self):
        is_empty = validator.validate_empty(self.name)
        if is_empty == validator.ErrorMessages.EMPTY_VAL:
            self.errors["name"]= _empty_val
            return
        is_not_valid = validator.validate_length(self.name, 50)
        if is_not_valid == validator.ErrorMessages.TOO_LONG:
            self.errors["name"]= _too_long

    def validate(self):
        self.errors = {}
        self.validate_name()
        return self.errors

    def get_data(self):
        d = {
            "id": self.id,
            "name": self.name
        }
        return d

    def to_json(self):
        return json.dumps(self.get_data())

Base.metadata.create_all(engine)