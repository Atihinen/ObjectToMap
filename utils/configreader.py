from ConfigParser import ConfigParser
from os import path

def get_configs(file, section):
    if not path.isfile(file):
        raise IOError("FIle {} not found".format(file))
    config = ConfigParser()
    config.read(file)
    opts = {}
    for opt in config.options(section):
        opts[opt] = config.get(section, opt)
    return opts

def get_db_configs():
    return get_configs("./db_config.ini", "db")