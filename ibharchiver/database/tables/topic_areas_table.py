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

class TopicAreasTable:
    CREATE_TABLE_CMD = 'CREATE TABLE IF NOT EXISTS TopicAreas' \
            ' (taId   INTEGER PRIMARY KEY ASC,' \
             ' taName TEXT NOT NULL UNIQUE);'
    TOPIC_AREAS = ('Christian Living', 'Church Life', 'Outreach', 'Salvation',
                   'Theology')

    def __init__(self, db_cursor):
        self.db_cursor = db_cursor

        self.db_cursor.execute(self.CREATE_TABLE_CMD)

        if not self.db_cursor.execute('SELECT * FROM TopicAreas;').fetchall():
            for topic_area in self.TOPIC_AREAS:
                self.db_cursor.execute('INSERT INTO TopicAreas (taName) VALUES (?);', (topic_area,))

        self.cache = dict()
        for topic_area_row in self.db_cursor.execute('SELECT * FROM TopicAreas;'):
            self.cache[topic_area_row[1]] = int(topic_area_row[0])

    def get_topic_area_by_id(self, ta_id):
        tmp_keys = list(self.cache.keys())
        tmp_values = list(self.cache.values())
        return tmp_keys[tmp_values.index(ta_id)]

    def get_topic_area_id(self, topic_area):
        return self.cache[topic_area]

    def get_topic_areas(self):
        return sorted(list(self.cache.keys()))
