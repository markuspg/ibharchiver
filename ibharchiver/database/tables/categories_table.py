class CategoriesTable:
    CREATE_TABLE_CMD = 'CREATE TABLE IF NOT EXISTS Categories' \
            ' (cId   INTEGER PRIMARY KEY ASC,' \
             ' cName TEXT NOT NULL UNIQUE)'

    def __init__(self, db_cursor):
        self.db_cursor = db_cursor

        self.db_cursor.execute(self.CREATE_TABLE_CMD)

        self.cache = dict()
        for category_row in self.db_cursor.execute('SELECT * FROM Categories;'):
            self.cache[category_row[1]] = int(category_row[0])

    def add_category(self, category):
        if category not in self.cache:
            self.db_cursor.execute('INSERT INTO Categories (cName) VALUES (?);', (category,))
            self.cache[category] = int(self.db_cursor.execute('SELECT cId FROM Categories WHERE cName = ?;', (category,)).fetchone()[0])

    def get_category_id(self, category):
        return self.cache[category]

    def get_categories(self):
        return self.cache.keys()
