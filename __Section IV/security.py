from user_model.usermodel import UserModel
from werkzeug.security import safe_str_cmp

users = [
    UserModel('hassouna', 'azerty', 1)
]


users_by_name = {user.username: user for user in users}

users_by_id = {user.id: user for user in users}


# this function checks if the username and pw are correct
# according to the pw and user in our db
# if true it returns the user
def authenticate(username, password):
    user = users_by_name.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


# this func returns user from their id
# TODO: to be investigated, still incomprehensible
def identity(payload):
    user = payload['identity']
    return users_by_id.get(user, None)
