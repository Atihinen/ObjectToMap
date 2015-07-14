__author__ = 'jjauhiainen'


from ConfigParser import ConfigParser
from os import path, remove
import sys
from getopt import getopt

class Manager():

    def __init__(self, verbose=None):
        self._db_conf = "db_config.ini"
        self.verbose = verbose
        self._list_of_actions = [
                "init_db_config",
                "delete_db_config"
                ]


    def run_action(self, action, **kwargs):
        print kwargs
        if action == "init_db_config":
            self.create_ini(kwargs["user"], kwargs["password"], kwargs["database"])
        elif action == "delete_db_config":
            self.delete_ini()
        else:
            print "No action {}. Complete list of actions: {}".format(action, ",".join(self._list_of_actions))


    def get_help(self, action):
        helps = {
            "init_db_config": self.create_ini_help(),
            "delete_db_config": self.delete_ini_help()
        }
        if action in helps:
            print helps.get(action)
        else:
            print "No help defined"


    def create_ini(self, user, password, db):
        if not user or not password or not db:
            print "Arguments: u: {}, p: {}, d: {}".format(user, password, db)
            print self.create_ini_help()
            return
        template = """
[db]
user={}
password={}
databse={}""".format(user, password, db)
        if path.isfile(self._db_conf):
            raise IOError("File {} already exists, delete it first".format(self._db_conf))
        with open(self._db_conf, "w") as f:
            f.write(template)
        if self.verbose:
            if path.isfile(self._db_conf):
                print "DB config created"

    def create_ini_help(self):
        return """Usage: python manage.py create_ini -u <user> -p <password> -d <database> (-v -h)
        -u --user:     database username
        -p --password: database password
        -d --database: database name
        Optional arguments
        -v --verbose:  prints debug messages
        -h --help:     prints this help
        """

    def delete_ini(self):
        if path.isfile(self._db_conf):
            try:
                remove(self._db_conf)
            except:
                print "Could not delete {}".format(self._db_conf)

    def delete_ini_help(self):
        return """Usage: python manage.py delete_db_config"""


def main():
    print sys.argv
    if len(sys.argv) == 1:
        print "Missing arguments"
        return
    action = sys.argv[1]
    verbose = None
    help_enabled = False
    username = None
    password = None
    database = None
    opts = None
    if len(sys.argv) > 2:
        try:
            opts, args = getopt(sys.argv[2:],"hh:v:u:p:d:",["--help", "--verbose", "--user=", "--password=", "--database="])
        except:
            pass
        print opts
        if opts:
            for opt, arg in opts:
                if opt == "-v" or opt == "--verbose":
                    verbose = "verbose"
                elif opt == "-h" or opt == "--help":
                    print "help"
                    help_enabled = True
                elif opt == "-u" or opt == "--user":
                    username = arg
                elif opt == "-p" or opt == "--password":
                    password = arg
                elif opt == "-d" or opt == "--database":
                    database = arg

    m = Manager(verbose)
    if help_enabled:
        m.get_help(action)
    else:
        m.run_action(action, user=username, password=password, database=database)


if __name__ == "__main__":
    main()