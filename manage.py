__author__ = 'jjauhiainen'


from ConfigParser import ConfigParser
from os import path, remove, walk, listdir
import sys
from getopt import getopt
from utils.connector import Darwin

class Manager():

    def __init__(self, verbose=None):
        self._db_conf = "db_config.ini"
        self.evolutions = "evolutions"
        self.verbose = verbose
        self._list_of_actions = [
                "init_db_config",
                "delete_db_config",
                "darwin",
                "init_db",
                "import_csv"
                ]


    def run_action(self, action, **kwargs):
        print kwargs
        if action == "init_db_config":
            if "port" in kwargs:
                if kwargs["port"]:
                    self.create_ini(kwargs["user"], kwargs["password"], kwargs["database"], kwargs["url"], kwargs["port"])
                    return
            self.create_ini(kwargs["user"], kwargs["password"], kwargs["database"], kwargs["url"])
        elif action == "delete_db_config":
            self.delete_ini()
        elif action == "darwin":
            self.run_migrations()
        elif action == "init_db":
            self.init_db()
        elif action == "import_csv":
            self.import_csv(kwargs["csvfile"])
        else:
            print "No action {}. Complete list of actions: {}".format(action, ",".join(self._list_of_actions))


    def get_help(self, action):
        helps = {
            "init_db_config": self.create_ini_help(),
            "delete_db_config": self.delete_ini_help(),
            "darwin": self.migration_help(),
            "init_db": self.init_db_help(),
            "import_csv": self.import_csv_help()
        }
        if action in helps:
            print helps.get(action)
        else:
            print "No help defined"


    def create_ini(self, user, password, db, url, port=3306):
        if not user or not password or not db or not url:
            print self.create_ini_help()
            return
        template = """
[db]
user={}
password={}
database={}
domain={}
port={}""".format(user, password, db, url, port)
        if path.isfile(self._db_conf):
            raise IOError("File {} already exists, delete it first".format(self._db_conf))
        with open(self._db_conf, "w") as f:
            f.write(template)
        if self.verbose:
            if path.isfile(self._db_conf):
                print "DB config created"

    def create_ini_help(self):
        return """Usage: python manage.py create_ini -u <user> -p <password> -d <database> -r <domain> (-o <port> -v -h)
        -u --user:     database username
        -p --password: database password
        -d --database: database name
        -r --url: domain/ip address for the mysql
        Optional arguments
        -o --port: mysql port, by default 3306
        -v --verbose:  prints debug messages
        -h --help:     prints this help
        """

    def import_csv_help(self):
        return """Usage: python manage.py import_csv -f <file>
        -f --file:  CSV file to be imported
        """

    def import_csv(self, csvfile):
        if not path.isfile(csvfile):
            raise IOError("File {} not found".format(csvfile))
        categories = self.get_categories()
        data = None
        with open(csvfile, "r") as f:
            data = f.readlines()[1:]
        for line in data:
            d = line.split(",")
            cat = d[3].lower()
            if not cat in categories:
                id = self.create_category(cat)
                categories[cat] = id
            lat = d[1]
            long = d[2]
            cat_id = categories[d[3].lower()]
            desc = ""
            try:
                desc = d[4].strip()
            except:
                pass
            trunk_line = ""
            try:
                trunk_line = d[5].strip()
            except:
                pass
            self.create_fire_hydrant(cat_id, lat, long, desc, trunk_line)


    def create_fire_hydrant(self, cat_id, lat, long, desc, trunk_line):
        d = Darwin()
        d.create_fire_hydrant(cat_id, lat, long, desc, trunk_line)

    def create_category(self, category_name):
        d = Darwin()
        id = d.create_category(category_name)
        return id

    def get_categories(self):
        d = Darwin()
        rows = d.get_categories()
        categories = {}
        if len(rows) > 1:
            for row in rows:
                categories[row[1]]=row[0]
        return categories


    def delete_ini(self):
        if path.isfile(self._db_conf):
            try:
                remove(self._db_conf)
            except:
                print "Could not delete {}".format(self._db_conf)

    def delete_ini_help(self):
        return """Usage: python manage.py delete_db_config"""

    def run_migrations(self):
        if not path.isdir(self.evolutions):
            print "Folder {} needs to exists".format(self.evolutions)
            return
        if len(listdir(self.evolutions)) == 0:
            print "Folder {} does not contain any files".format(self.evolutions)
        evolution_list = []
        for root, dirs, files in walk(self.evolutions):
            for file in files:
                if file.endswith(".sql"):
                    evolution_list.append(path.join(root,file))
        d = Darwin()
        d.run_queries_from_files(evolution_list)

    def migration_help(self):
        return """Usage: python manage.py darwin

        Runs SQL files in order from folder {}""".format(self.evolutions)

    def init_db(self):
        d = Darwin()
        d.init_db()

    def init_db_help(self):
        return """Usage: python manage.py init_db

        Creates table for evolution files"""

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
    url = None
    port = None
    opts = None
    csvfile = None
    if len(sys.argv) > 2:
        try:
            opts, args = getopt(sys.argv[2:],"hh:v:u:p:d:r:o:f:",["--help", "--verbose", "--user=", "--password=", "--database=", "--url=", "--port=", "--file="])
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
                elif opt == "-r" or opt == "--url":
                    url = arg
                elif opt == "-o" or opt == "--port":
                    port = arg
                elif opt == "-f" or opt == "--file":
                    csvfile = arg

    m = Manager(verbose)
    if help_enabled:
        m.get_help(action)
    else:
        m.run_action(action, user=username, password=password, database=database, url=url, port=port, csvfile=csvfile)


if __name__ == "__main__":
    main()