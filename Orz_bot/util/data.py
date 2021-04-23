import sqlite3
import os


from Orz_bot.constants import *


class Data:

    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)

        create_mutelist = 'CREATE TABLE IF NOT EXISTS mutelist (id integer, guild integer, mutetime real)'

        curr = self.get_curr()
        curr.execute(create_mutelist)
        self.conn.commit()

    def get_curr(self):
        # if self.conn.closed:
        #     print('Connection is closed. Restarting...')
        #     self.conn = sqlite3.connect(self.db_file)
        return self.conn.cursor()

    def get_mutetime(self, person: int, guild: int):
        sql = f'SELECT * FROM mutelist WHERE id={person} and guild={guild}'
        curr = self.get_curr()
        curr.execute(sql)
        rows = curr.fetchall()
        if len(rows) == 0:
            return None
        return rows[0][2]

    def mutelist(self):
        sql = f'SELECT * FROM mutelist'
        curr = self.get_curr()
        curr.execute(sql)
        rows = curr.fetchall()
        return rows

    def remove_mutetime(self, person: int, guild: int):
        sql = f'DELETE FROM mutelist WHERE id={person} and guild={guild}'
        curr = self.get_curr()
        curr.execute(sql)
        self.conn.commit()

    def change_mutetime(self, person: int, guild: int, mutetime: float):
        sql = f'INSERT INTO mutelist VALUES ({person}, {guild}, {mutetime})'

        curr = self.get_curr()
        curr.execute(sql)
        self.conn.commit()


data_manager = Data(os.path.join(DB_DIR, 'data.db'))
