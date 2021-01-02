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

import lzma
import time

class ItemsTable:
    CREATE_TABLE_CMD = 'CREATE TABLE IF NOT EXISTS Items' \
            ' (type INTEGER,' \
            '  title TEXT NOT NULL,' \
            '  bytes BLOB NOT NULL UNIQUE,' \
            '  author INTEGER,' \
            '  categories TEXT NOT NULL,' \
            '  topics TEXT,' \
            '  comments TEXT,' \
            '  book INTEGER,' \
            '  chapters INTEGER,' \
            '  verses INTEGER,' \
            '  filename TEXT,' \
            '  importDate INTEGER,' \
            '  lastExportDate INTEGER,' \
            '  lastPlayDate INTEGER,' \
            '  uncompressedSize INTEGER NOT NULL,' \
            '  compressedSize INTEGER NOT NULL,' \
            '  FOREIGN KEY(author) REFERENCES Authors(aId),' \
            '  FOREIGN KEY (book) REFERENCES BibleBooks(bId),' \
            '  FOREIGN KEY(type) REFERENCES ResourceTypes(rId)' \
            '  UNIQUE(title, type));'

    def __init__(self, db_cursor):
        self.db_cursor = db_cursor

        self.db_cursor.execute(self.CREATE_TABLE_CMD)

    """
    Retrieve information about all resoures stored in the database

    Returns:
        A list of tuples containing each item's resource type, title, autor, category and topic
    """
    def get_items_info(self):
        item_infos = list()

        res = self.db_cursor.execute('SELECT rName, title, aName, categories, topics FROM Items INNER JOIN Authors ON Authors.aId = Items.author INNER JOIN ResourceTypes ON ResourceTypes.rId = Items.type;').fetchall()
        for re in res:
            categories = list()
            topics = list()
            for c_id in [int(c_id_s) for c_id_s in re[3].split(',')]:
                categories.append(self.db_cursor.execute('SELECT cName FROM Categories WHERE cId = ?;', (c_id,)).fetchone()[0])
            if re[4]:
                for t_id in [int(t_id_s) for t_id_s in re[4].split(',')]:
                    topics.append(self.db_cursor.execute('SELECT tName FROM Topics WHERE tId = ?;', (re[4],)).fetchone()[0])
            item_infos.append((re[0], re[1], re[2], ', '.join(categories), ', '.join(topics)))

        return item_infos


    """
    Retrieve a specific resource from the database

    Parameters:
        resource_type: The resource type of the requested item
        title: The title of the requested item

    Returns:
        A tuple of the resource's bytes, its filename and its size
    """
    def get_resource(self, resource_type, title):
        r_id = self.db_cursor.execute('SELECT rId FROM ResourceTypes WHERE rName = ?;', (resource_type,)).fetchone()[0]
        res = self.db_cursor.execute('SELECT bytes, filename, uncompressedSize from Items WHERE type = ? AND title = ?;', (r_id, title)).fetchone()
        return lzma.decompress(res[0]), res[1], res[2]

    def add_resource(self, r_id, title, data_bytes, a_id, c_ids, t_ids, b_id, chapters, verses, filename):
        uncompressed_size = len(data_bytes)
        compressed_bytes = lzma.compress(data_bytes, lzma.FORMAT_XZ, lzma.CHECK_SHA256, 9 | lzma.PRESET_EXTREME)
        compressed_size = len(compressed_bytes)
        topics = None
        if t_ids:
            topics = ','.join([str(t_id) for t_id in t_ids])
        self.db_cursor.execute('INSERT INTO Items (type, title, bytes, author, categories, topics, book, chapters, verses, filename, importDate, uncompressedSize, compressedSize) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (r_id, title, compressed_bytes, a_id, ','.join([str(c_id) for c_id in c_ids]), topics, b_id, chapters, verses, filename, int(time.time()), uncompressed_size, compressed_size))
