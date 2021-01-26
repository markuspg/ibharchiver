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

class TopicsTable:
    CREATE_TABLE_CMD = 'CREATE TABLE IF NOT EXISTS Topics' \
            ' (tId   INTEGER PRIMARY KEY ASC,' \
             ' tName TEXT NOT NULL UNIQUE,' \
             ' tArea INTEGER,' \
             ' FOREIGN KEY (tArea) REFERENCES TopicAreas(taId));'
    TOPICS = {'Christian Living': ('Assurance', 'Bible Reading', 'Conscience',
                                   'Death & Dying', 'Depression',
                                   'Drinking Alcohol', 'Encouragement',
                                   'Fasting', 'Feelings', 'Forgiveness',
                                   'Hospitality', 'Joy', "Knowing God's Will",
                                   'Legalism', 'Modesty', 'Money & Stewardship',
                                   'Music', 'Prayer', 'Pride & Humility',
                                   'Providence', 'Sabbath', 'Speech & Tongue',
                                   'Suffering', 'Temptation', 'The Law',
                                   'Work & Vacation', 'Worldliness'),
              'Church Life': ('Baptism', 'Christian Unity', 'Church Discipline',
                              'Church History / Biographies', 'Church Planting',
                              'Corporate Prayer', 'Pastors & Elders',
                              'Preaching', 'Revival', 'Spiritual Gifts',
                              'The Church', "The Lord's Supper",
                              "Woman's Roles"),
              'Outreach': ('Apologetics', 'Evangelism', 'Evangelizing Children',
                           'Missions', 'Open-Air Preaching', 'Tracts',
                           'Witnessing to Lost Family'),
              'Salvation': ('Adoption', 'End Times', 'Examine Yourself',
                            'Faith', 'Heaven', 'Hell', 'Justification',
                            'Lordship', 'Once Saved Always Saved?',
                            'Regeneration / Born Again', 'Repentance',
                            'Sanctification', 'The Gospel'),
              'Theology': ('God', 'Jesus Christ', 'The Fear of God',
                           'The Holiness of God', 'The Holy Spirit',
                           'The Love of God', 'The Sovereignty of God',
                           'The Trinity', 'The Wrath of God')}

    def __init__(self, db_cursor, ta_table):
        self.db_cursor = db_cursor
        self.ta_table = ta_table

        self.db_cursor.execute(self.CREATE_TABLE_CMD)

        if not self.db_cursor.execute('SELECT * FROM Topics;').fetchall():
            for cat, tops in self.TOPICS.items():
                for top in tops:
                    self.db_cursor.execute('INSERT INTO Topics (tName, tArea) VALUES (?, ?);', (top, ta_table.get_topic_area_id(cat)))

        self.cache = dict()
        for topic_row in self.db_cursor.execute('SELECT * FROM Topics;'):
            self.cache[topic_row[1]] = int(topic_row[0])

    def add_topic(self, topic, topic_area):
        if topic not in self.cache:
            t_area_id = self.ta_table.get_topic_area_id(topic_area)
            self.db_cursor.execute('INSERT INTO Topics (tName, tArea) VALUES (?, ?);', (topic, t_area_id))
            self.cache[topic] = int(self.db_cursor.execute('SELECT tId FROM Topics WHERE tName = ?;', (topic,)).fetchone()[0])

    def get_topic_by_id(self, t_id):
        tmp_keys = list(self.cache.keys())
        tmp_values = list(self.cache.values())
        return tmp_keys[tmp_values.index(t_id)]

    def get_topic_id(self, topic):
        return self.cache[topic]

    def get_topics(self):
        return sorted(list(self.cache.keys()))
