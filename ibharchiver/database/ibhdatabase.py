import sqlite3

from database.tables.authors_table import AuthorsTable
from database.tables.bible_books_table import BibleBooksTable
from database.tables.categories_table import CategoriesTable
from database.tables.items_table import ItemsTable
from database.tables.metadata_table import MetadataTable
from database.tables.resource_types_table import ResourceTypesTable
from database.tables.topics_table import TopicsTable

class IBHDatabase:
    def __init__(self):
        self.db_conn = sqlite3.connect('/home/maprasser/test.db')
        self.db_cursor = self.db_conn.cursor()

        self._create_tables()

    def _create_tables(self):
        self.authors_table = AuthorsTable(self.db_cursor)
        self.bible_books_table = BibleBooksTable(self.db_cursor)
        self.categories_table = CategoriesTable(self.db_cursor)
        self.items_table = ItemsTable(self.db_cursor)
        self.metadata_table = MetadataTable(self.db_cursor)
        self.resource_types_table = ResourceTypesTable(self.db_cursor)
        self.topics_table = TopicsTable(self.db_cursor)

        self.db_conn.commit()
