from os.path import dirname, abspath, os
import sqlite3

# using abspath otherwise it would use / instead of \ before fist_db.db
# first dirname is to get rid of the file name
# second dirnam is to get red of the dir name i.e. user_api (currently)

path = os.path.join(dirname(dirname(abspath(__file__))), 'first_db.db')


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        db = sqlite3.connect(path)
        cursor = db.cursor()
        query = 'SELECT * FROM users WHERE username=?'
        result = cursor.execute(query, (username,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        db.close()

        return user

    @classmethod
    def find_by_id(cls, _id):

        db = sqlite3.connect(path)
        cursor = db.cursor()
        query = 'SELECT * FROM users WHERE id=?'
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        db.close()

        return user
