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
