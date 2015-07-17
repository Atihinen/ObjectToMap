import MySQLdb as mdb
from utils.configreader import get_db_configs

class Darwin():

    def __init__(self):
        self.db_config = get_db_configs()
        self.con = None
        self.create_connection()

    def create_connection(self):
        port = int(self.db_config['port'])
        self.con = mdb.connect(host=self.db_config['domain'],
                               user=self.db_config['user'],
                               passwd=self.db_config['password'],
                               db=self.db_config['database'],
                               port=port)

    def run_queries_from_files(self, files):
        for f in files:
            with open(f, 'r') as f:
                sql = "".join(f.readlines())
                try:
                    cursor = self.con.cursor()
                    cursor.execute(sql)
                except mdb.Error, e:
                    print "Error {}: {}".format(e.args[0], e.args[1:])
        self.close_connection()

    def close_connection(self):
        if self.con:
            self.con.close()
            self.con = None