import sqlite3

class IBHDatabase:
    def __init__(self):
        self.db_conn = sqlite3.connect('/home/maprasser/test.db')
        self.db_cursor = self.db_conn.cursor()
