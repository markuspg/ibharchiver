class MetadataTable:
    CREATE_TABLE_CMD = 'CREATE TABLE IF NOT EXISTS Metadata' \
            ' (mdKey TEXT NOT NULL UNIQUE,' \
             ' mdValue TEXT NOT NULL UNIQUE);'
    DB_SCHEME_VERSION = 1

    def __init__(self, db_cursor):
        self.db_cursor = db_cursor

        self.db_cursor.execute(self.CREATE_TABLE_CMD)

        if not self.db_cursor.execute('SELECT * FROM Metadata;').fetchall():
            self.db_cursor.execute('INSERT INTO Metadata VALUES (?, ?);',
                    ('DB_SCHEME_VERSION', self.DB_SCHEME_VERSION))
