from os.path import dirname, abspath, os
import sqlite3
from db import dbalch

# using abspath otherwise it would use / instead of \ before fist_db.db
# first dirname is to get rid of the file name
# second dirnam is to get red of the dir name i.e. user_api (currently)

path = os.path.join(dirname(dirname(abspath(__file__))), 'first_db.db')


class UserModel(dbalch.Model):

    __tablename__ = "users"

    id = dbalch.Column(dbalch.Integer, primary_key=True)
    username = dbalch.Column(dbalch.String(256))
    password = dbalch.Column(dbalch.String(256))

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    # this converts a UserModel to a json/dict object
    def user_to_json(self):
        return {"id": self.id, "username": self.username, "password": self.password}

    # this method returns a UserModel object from a json object
    @classmethod
    def json_to_user(cls, user_json):

        username = user_json.get('username', None)
        assert type(username) == str, "assertion failed, username should be a string"
        password = user_json.get('password', None)
        assert type(password) == str, "assertion failed, password should be a string"
        id = user_json.get('id', None)
        assert type(id) == int, "assertion failed, id is not an integer"

        return cls(username=username, password=password, id=id)

    # this method converts tuples (rows) to json
    @staticmethod
    def from_tuple_to_json(user_tuple):
        if tuple:
            return {"id": user_tuple[0], "username": user_tuple[1], "password": user_tuple[2]}
        else:
            return None

    @classmethod
    def find_by_username(cls, username):
        result = cls.query.filter_by(username=username).first()
        if result:
            return result
        else:
            return None

    @classmethod
    def find_by_id(cls, id):
        result = cls.query.filter_by(id=id).first()
        if result:
            return result
        else:
            return None

    def post_user_to_db(self):
        user = UserModel.find_by_username(self.username)
        if not user:
            dbalch.session.add(self)
            dbalch.session.commit()
            return True
        else:
            return False

    def update_user_to_db(self):
        dbalch.session.add(self)
        dbalch.session.commit()

    def delete_user(self):
        dbalch.session.delete(self)
        dbalch.session.commit()