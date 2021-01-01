class AuthorsTable:
    CREATE_TABLE_CMD = 'CREATE TABLE IF NOT EXISTS Authors' \
            ' (aId   INTEGER PRIMARY KEY ASC,' \
             ' aName TEXT NOT NULL UNIQUE);'

    def __init__(self, db_cursor):
        self.db_cursor = db_cursor

        self.db_cursor.execute(self.CREATE_TABLE_CMD)

        self.cache = dict()
        for author_row in self.db_cursor.execute('SELECT * FROM Authors;'):
            self.cache[author_row[1]] = int(author_row[0])

    def add_author(self, author):
        if author not in self.cache:
            self.db_cursor.execute('INSERT INTO Authors (aName) VALUES (?);', (author,))
            self.cache[author] = int(self.db_cursor.execute('SELECT aId FROM Authors WHERE aName = ?;', (author,)).fetchone()[0])

    def get_author_id(self, author):
        return self.cache[author]

    def get_authors(self):
        return self.cache.keys()
