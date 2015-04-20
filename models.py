from lib.db import Base
from sqlalchemy import Column, Integer, Sequence, String
class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name.lower()



"""class FireHydrant(Base):
    __tablename__ = 'fire_hydrant'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    name = Column(String(50))


    def __init__(self, name=None):
        self.validate_name(name)


    def validate_name(self, name):
        if name:
            if len(name) > 50:
                raise ValueError("Name can only be 50 characters, name was {} long".format(len(name)))
            self.name = name
            """