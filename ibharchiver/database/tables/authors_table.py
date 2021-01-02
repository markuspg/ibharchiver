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

class AuthorsTable:
    CREATE_TABLE_CMD = 'CREATE TABLE IF NOT EXISTS Authors' \
            ' (aId   INTEGER PRIMARY KEY ASC,' \
             ' aName TEXT NOT NULL UNIQUE);'

    def __init__(self, db_cursor, authors_model):
        self.authors_model = authors_model
        self.db_cursor = db_cursor

        self.db_cursor.execute(self.CREATE_TABLE_CMD)

        self.cache = dict()
        for author_row in self.db_cursor.execute('SELECT * FROM Authors;'):
            self.cache[author_row[1]] = int(author_row[0])
            self.authors_model.append([author_row[1]])

    def add_author(self, author):
        if author not in self.cache:
            self.db_cursor.execute('INSERT INTO Authors (aName) VALUES (?);', (author,))
            self.cache[author] = int(self.db_cursor.execute('SELECT aId FROM Authors WHERE aName = ?;', (author,)).fetchone()[0])
            self.authors_model.append([author])

    def get_author_id(self, author):
        return self.cache[author]

    def get_authors(self):
        return sorted(list(self.cache.keys()))
