class ResourceTypesTable:
    CREATE_TABLE_CMD = 'CREATE TABLE IF NOT EXISTS ResourceTypes' \
            ' (rId   INTEGER PRIMARY KEY ASC,' \
             ' rName TEXT NOT NULL UNIQUE);'
    RESOURCE_TYPES = ('HTML', 'MP3', 'PDF')

    def __init__(self, db_cursor):
        self.db_cursor = db_cursor

        self.db_cursor.execute(self.CREATE_TABLE_CMD)

        if not self.db_cursor.execute('SELECT * FROM ResourceTypes;').fetchall():
            for resource_type in self.RESOURCE_TYPES:
                self.db_cursor.execute('INSERT INTO ResourceTypes (rName) VALUES (?);', (resource_type,))

        self.cache = dict()
        for resource_type_row in self.db_cursor.execute('SELECT * FROM ResourceTypes;'):
            self.cache[resource_type_row[1]] = int(resource_type_row[0])

    def get_resource_type_id(self, resource_type):
        return self.cache[resource_type]

    def get_resource_types(self):
        return sorted(list(self.cache.keys()))
