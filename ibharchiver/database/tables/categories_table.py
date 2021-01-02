# MIT License
#
# Copyright (c) 2020-2021 Markus Prasser
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

class CategoriesTable:
    CREATE_TABLE_CMD = 'CREATE TABLE IF NOT EXISTS Categories' \
            ' (cId   INTEGER PRIMARY KEY ASC,' \
             ' cName TEXT NOT NULL UNIQUE);'

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
        return sorted(list(self.cache.keys()))
