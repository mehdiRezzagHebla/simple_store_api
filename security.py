from user_model.usermodel import UserModel
from werkzeug.security import safe_str_cmp


# this function checks if the username and pw are correct
# according to the pw and user in our db
# if true it returns the user
def authenticate(username, password):
    print("authenticate was called.")
    user = UserModel.find_by_username(username)
    print(user)
    if user and safe_str_cmp(user.password, password):
        return user


# this func returns user from their id
# TODO: to be investigated, still incomprehensible
def identity(payload):
    user = payload['identity']
    return UserModel.find_by_id(user)
