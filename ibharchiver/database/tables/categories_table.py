class CategoriesTable:
    CREATE_TABLE_CMD = 'CREATE TABLE IF NOT EXISTS Categories' \
            ' (cId   INTEGER PRIMARY KEY ASC,' \
             ' cName TEXT NOT NULL UNIQUE)'

    def __init__(self, db_cursor):
        self.db_cursor = db_cursor

        self.db_cursor.execute(self.CREATE_TABLE_CMD)
