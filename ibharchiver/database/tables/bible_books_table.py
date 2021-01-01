class BibleBooksTable:
    BIBLE_BOOKS = ('Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy',
                   'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel',
                   '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra',
                   'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs',
                   'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah',
                   'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos',
                   'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk',
                   'Zephaniah', 'Haggai', 'Zechariah', 'Malachi', 'Matthew',
                   'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians',
                   '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians',
                   'Colossians', '1 Thessalonians', '2 Thessalonians',
                   '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews',
                   'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John',
                   'Jude', 'Revelation')
    CREATE_TABLE_CMD = 'CREATE TABLE IF NOT EXISTS BibleBooks' \
            ' (bId   INTEGER PRIMARY KEY ASC,' \
             ' bName TEXT NOT NULL UNIQUE)'

    def __init__(self, db_cursor):
        self.db_cursor = db_cursor

        self.db_cursor.execute(self.CREATE_TABLE_CMD)

        if not self.db_cursor.execute('SELECT * FROM BibleBooks').fetchall():
            for bible_book in self.BIBLE_BOOKS:
                self.db_cursor.execute('INSERT INTO BibleBooks (bName) VALUES (?)', (bible_book,))

        self.cache = dict()
        for bible_book_row in self.db_cursor.execute('SELECT * FROM BibleBooks;'):
            self.cache[bible_book_row[1]] = int(bible_book_row[0])

    def get_bible_books(self):
        return [x[0] for x in sorted(list(self.cache.items()), key=lambda item: item[1])]

    def get_bible_book_id(self, bible_book):
        return self.cache[bible_book]
