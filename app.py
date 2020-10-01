from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
import security
from user_api.user_api import Reg_User, UserList
from item_api.item_api import Item, ItemList
from store_api.store_api import Store

# this line is a must in any flask app
app = Flask(__name__)

# this is like an encrypting code
# somehow it prevents tempering with cookies
app.secret_key = 'joumanji'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///first_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
api.add_resource(Reg_User, '/reg_user/<string:name>', endpoint='kk')
api.add_resource(Reg_User, '/reg_user', endpoint='lamcha')
api.add_resource(UserList, '/users')
api.add_resource(Store, '/store', endpoint='get or set')
api.add_resource(Store, '/stores', endpoint='all stores')

if __name__ == '__main__':
    from db import dbalch
    dbalch.init_app(app)
    app.run(debug=True, port=5000)
