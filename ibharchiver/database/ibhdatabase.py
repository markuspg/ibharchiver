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

import sqlite3

from database.tables.authors_table import AuthorsTable
from database.tables.bible_books_table import BibleBooksTable
from database.tables.categories_table import CategoriesTable
from database.tables.items_table import ItemsTable
from database.tables.metadata_table import MetadataTable
from database.tables.resource_types_table import ResourceTypesTable
from database.tables.topic_areas_table import TopicAreasTable
from database.tables.topics_table import TopicsTable

class IBHDatabase:
    def __init__(self, authors_model):
        self.db_conn = sqlite3.connect('/home/maprasser/test.db')
        self.db_cursor = self.db_conn.cursor()

        self._create_tables(authors_model)

    def _create_tables(self, authors_model):
        self.authors_table = AuthorsTable(self.db_cursor, authors_model)
        self.bible_books_table = BibleBooksTable(self.db_cursor)
        self.categories_table = CategoriesTable(self.db_cursor)
        self.items_table = ItemsTable(self.db_cursor)
        self.metadata_table = MetadataTable(self.db_cursor)
        self.resource_types_table = ResourceTypesTable(self.db_cursor)
        self.topic_areas_table = TopicAreasTable(self.db_cursor)
        self.topics_table = TopicsTable(self.db_cursor)

        self.db_conn.commit()
