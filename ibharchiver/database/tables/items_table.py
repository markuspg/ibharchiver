import lzma
import time

class ItemsTable:
    CREATE_TABLE_CMD = 'CREATE TABLE IF NOT EXISTS Items' \
            ' (type INTEGER,' \
            '  title TEXT NOT NULL,' \
            '  bytes BLOB NOT NULL,' \
            '  author INTEGER,' \
            '  category INTEGER,' \
            '  topic INTEGER,' \
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
            '  FOREIGN KEY(category) REFERENCES Categories(cId),' \
            '  FOREIGN KEY(topic) REFERENCES Topics(tId),' \
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

        res = self.db_cursor.execute('SELECT rName, title, aName, cName, topic FROM Items INNER JOIN Authors ON Authors.aId = Items.author INNER JOIN Categories ON Categories.cId = Items.category INNER JOIN ResourceTypes ON ResourceTypes.rId = Items.type;')
        for re in res:
            if re[4]:
                topic = self.db_cursor.execute('SELECT tName FROM Topics WHERE tId = ?;', (re[4],)).fetchone()[0]
            else:
                topic = str()
            item_infos.append((re[0], re[1], re[2], re[3], topic))

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

    def add_resource(self, r_id, title, data_bytes, a_id, c_id, t_id, b_id, chapters, verses, filename):
        uncompressed_size = len(data_bytes)
        compressed_bytes = lzma.compress(data_bytes, lzma.FORMAT_XZ, lzma.CHECK_SHA256, 9 | lzma.PRESET_EXTREME)
        compressed_size = len(compressed_bytes)
        self.db_cursor.execute('INSERT INTO Items (type, title, bytes, author, category, topic, book, chapters, verses, filename, importDate, uncompressedSize, compressedSize) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (r_id, title, compressed_bytes, a_id, c_id, t_id, b_id, chapters, verses, filename, int(time.time()), uncompressed_size, compressed_size))
