# -*- coding: utf-8 -*-
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from utils.configreader import get_db_configs
db_config = get_db_configs()
Base = declarative_base()
engine = create_engine('mysql://{}:{}@{}:{}/{}?charset=utf8'.format(db_config["user"], db_config["password"], db_config["domain"], db_config["port"], db_config["database"]), echo=False)
plugin = sqlalchemy.Plugin(
    engine, # SQLAlchemy engine created with create_engine function.
    Base.metadata, # SQLAlchemy metadata, required only if create=True.
    keyword='db', # Keyword used to inject session database in a route (default 'db').
    create=True, # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
    commit=True, # If it is true, plugin commit changes after route is executed (default True).
    use_kwargs=False # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
)
from sqlalchemy.orm import sessionmaker

def create_session():
    Session = sessionmaker(bind=engine)
    return Session()
db = create_session()