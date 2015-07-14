__author__ = 'jjauhiainen'


from ConfigParser import ConfigParser
from os import path, remove
import sys
from getopt import getopt

class Manager():

    def __init__(self, verbose=None):
        self._db_conf = "db_config.ini"
        self.verbose = verbose

    def create_ini(self, user, password, db):
        if not user or not password or not db:
            raise ValueError("Missing arguments. user={}, password={}, db={}".format(user, password, db))
        template = \
            """[db]
            user={}
            password={}
            databse={}
            """.format(user, password, db)
        if path.isfile(self._db_conf):
            raise IOError("File {} already exists, delete it first".format(self._db_conf))
        with open(self._db_conf, "w") as f:
            f.write(template)
        if self.verbose:
            if path.isfile(self._db_conf):
                print "DB config created"

    def create_ini_help(self):
        print """Usage: python manage.py create_ini

        """

    def delete_ini(self):
        if path.isfile(self._db_conf):
            try:
                remove(self._db_conf)
            except:
                print "Could not delete {}".format(self._db_conf)


def main():
    print sys.argv
    if len(sys.argv) == 1:
        print "Missing arguments"
        return
    action = sys.argv[1]
    verbose = None
    opts = None
    if len(sys.argv) > 2:
        try:
            opts, args = getopt(sys.argv[2:],"hv:",["--help", "--verbose"])
        except:
            pass
        print opts
        if opts:
            for opt, arg in opts:
                if opt == "-v" or opt == "--verbose":
                    verbose = "verbose"
                elif opt == "-h" or opt == "--help":
                    print "This is help"

if __name__ == "__main__":
    main()