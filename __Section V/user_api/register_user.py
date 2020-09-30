from flask_restful import Resource, reqparse
import sqlite3
from user_model.usermodel import path, UserModel


class Reg_User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='Username is required'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='Password is required',
    )

    def post(self):
        # retrieving info from json request content
        args = Reg_User.parser.parse_args()
        username = args['username']
        password = args['password']

        db = sqlite3.connect(path)
        cursor = db.cursor()
        user = UserModel.find_by_username(username)
        if user:
            db.close()
            return {"message": f"the username {username} is not available"}, 400
        else:
            insert_user_query = 'INSERT INTO users (username, password) VALUES (?, ?)'
            cursor.execute(insert_user_query, (username, password))
            db.commit()
            result = UserModel.find_by_username(username)

            json_return = {
                'username': result.username,
                'password': result.password
            }

            db.close()

            return json_return, 201



