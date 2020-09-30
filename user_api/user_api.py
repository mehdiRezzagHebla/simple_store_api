from flask_restful import Resource, reqparse
from user_model.usermodel import UserModel


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

        user_to_post = UserModel(username=username, password=password, id=None)
        query = user_to_post.post_user_to_db()
        if query:
            return user_to_post.user_to_json(), 201
        else:
            return {"message": f"the username {username} is not available"}, 400


    def get(self, name):
        args = Reg_User.parser.parse_args()
        result = UserModel.find_by_username(name)
        if result:
            user_dict = result.user_to_json()
            return user_dict, 200
        else:
            return {"message": f"No user named {name} was found."}, 404

    def delete(self):
        args = Reg_User.parser.parse_args()
        name = args['username']
        pw = args['password']
        result = UserModel.find_by_username(name)
        if result:
            result.delete_user()
            message = {"message": f'user {name} deleted successfully'}
            message.update(result.user_to_json())
            return message, 201
        else:
            return {"message": f"user {name} was not found"}, 404


class UserList(Resource):

    def get(self):
        all_users = UserModel.query.all()
        list_of_user_json = []
        if all_users:
            for user in all_users:
                list_of_user_json.append(user.user_to_json())
            return {"list_of_all_users": list_of_user_json}, 200
        else:
            return {"message": "no users could be found in the database."}, 404

