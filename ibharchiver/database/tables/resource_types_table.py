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
