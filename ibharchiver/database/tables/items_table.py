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
            '  UNIQUE(title, type))'

    def __init__(self, db_cursor):
        self.db_cursor = db_cursor

        self.db_cursor.execute(self.CREATE_TABLE_CMD)
