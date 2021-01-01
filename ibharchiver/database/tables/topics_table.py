class TopicsTable:
    CREATE_TABLE_CMD = 'CREATE TABLE IF NOT EXISTS Topics' \
            ' (tId   INTEGER PRIMARY KEY ASC,' \
             ' tName TEXT NOT NULL UNIQUE);'

    def __init__(self, db_cursor):
        self.db_cursor = db_cursor

        self.db_cursor.execute(self.CREATE_TABLE_CMD)

        self.cache = dict()
        for topic_row in self.db_cursor.execute('SELECT * FROM Topics;'):
            self.cache[topic_row[1]] = int(topic_row[0])

    def add_topic(self, topic):
        if topic not in self.cache:
            self.db_cursor.execute('INSERT INTO Topics (tName) VALUES (?);', (topic,))
            self.cache[topic] = int(self.db_cursor.execute('SELECT tId FROM Topics WHERE tName = ?;', (topic,)).fetchone()[0])

    def get_topic_by_id(self, t_id):
        tmp_keys = list(self.cache.keys())
        tmp_values = list(self.cache.values())
        return tmp_keys[tmp_values.index(t_id)]

    def get_topic_id(self, topic):
        return self.cache[topic]

    def get_topics(self):
        return self.cache.keys()
