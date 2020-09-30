from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
import security
from user_api.user_api import Reg_User
from item_api.item_api import Item, ItemList

# this line is a must in any flask app
app = Flask(__name__)

# this is like an encrypting code
# somehow it prevents tempering with cookies
app.secret_key = 'joumanji'

# initializes the API?
api = Api(app)

# used to get a json web token?
# it generates an entry point /auth
# we send it a user & pw and it sends us back a jwt
# afterwards, whenever we send a request we have to send the jwt
# upon request, the JWT class checks the identity from the token and if a user is returned
# the request is carried
# ofc, any request that should be secured with a token should have the decorator
# @jwt_required()
jwt = JWT(app=app, authentication_handler=security.authenticate, identity_handler=security.identity)



# add resource creates an entry point
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/item')
api.add_resource(Reg_User, '/reg_user')

if __name__ == '__name__':
    app.run(debug=True, port=5000)
