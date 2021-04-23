import sqlite3


class Data:

    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)

        create_mutelist = 'CREATE TABLE IF NOT EXISTS mutelist (id integer UNIQUE PRIMARY KEY, enddate real)'

        curr = self.get_curr()
        curr.execute(create_mutelist)
        self.conn.commit()

    def get_curr(self):
        if self.conn.closed:
            print('Connection is closed. Restarting...')
            self.conn = sqlite3.connect(self.db_file)
        return self.conn.cursor()

    def get_mutetime(self, person: int):
        sql = f'SELECT FROM mutelist WHERE id={person}'
        curr = self.get_curr()
        curr.execute(sql)
        rows = curr.fetchall()
        if len(rows) == 0:
            return None
        return rows[0]


data_manager = Data()
