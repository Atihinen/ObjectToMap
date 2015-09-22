__author__ = 'jjauhiainen'
import unicodecsv as csv
import codecs
#import csv
import os
from datetime import datetime
import calendar

class CSVWriter():
    def __init__(self):
        _timestamp = calendar.timegm(datetime.utcnow().utctimetuple())
        self.file = "{}_csv.csv".format(_timestamp)
        self.path = os.path.join(os.sep, "tmp", self.file)

    def write_csv(self, rows):
        with open(self.path, "wb") as f:
            f.write(codecs.BOM_UTF8)
            writer = csv.writer(f, encoding='UTF-8')
            writer.writerows(rows)
        return self.file, self.path