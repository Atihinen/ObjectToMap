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
        evolutions = self.get_evolutions()
        self.create_connection()
        for f in files:
            if not f in evolutions:
                with open(f, 'r') as data:
                    sql = "".join(data.readlines())
                    try:
                        cursor = self.con.cursor()
                        cursor.execute(sql)
                    except mdb.Error, e:
                        print "Error {}: {}".format(e.args[0], e.args[1:])
                    evolution_sql = "INSERT INTO evolutions (file_name) VALUES ('{}')".format(f)
                    print evolution_sql
                    try:
                        cursor = self.con.cursor()
                        cursor.execute(evolution_sql)
                        self.con.commit()
                    except mdb.Error, e:
                        self.con.rollback()
                        print "Error {}: {}".format(e.args[0], e.args[1:])
        self.close_connection()

    def get_evolutions(self):
        result = None
        try:
            cursor = self.con.cursor()
            sql = "SELECT file_name from evolutions;"
            cursor.execute(sql)
            result = cursor.fetchall()
        except mdb.Error, e:
            print "Error {}: {}".format(e.args[0], e.args[1:])
        self.close_connection()
        if len(result) == 0:
            return ()
        return result[0]

    def init_db(self):
        sql= """CREATE TABLE evolutions (
        id INT(255) NOT NULL AUTO_INCREMENT,
        file_name VARCHAR(50),
        PRIMARY KEY (id)
        )
        """
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