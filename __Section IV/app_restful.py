from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
import security

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


items = []


# the Resource inheritance allows for handling the conversion dict-json I guess
# also Resource allows for specifying the HTTP verb just by overwriting get/post/delete, etc.
# this class is used to create an item and to retrieve an item
class Item(Resource):
    # this is my parser used to maintain a strongly typed map
    parser = reqparse.RequestParser()
    # adding arguments as to what should be included as argument
    # even if the json object contains other key-value pairs
    # they will not be included unless add_argument was called on them
    # in this case only "price": xxx.xx is included
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank')

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return item, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {"message": f"the item {name} already exists"}, 400

        args = Item.parser.parse_args()
        # got replaced by parser, which allows for strongly typed data
        # get_data = request.get_json()
        item = {"name": name, "price": args['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return items

    def put(self, name):

        # this replaces the request.get_json()
        # and returns only the arguments provided in add_argument
        args = Item.parser.parse_args()

        # retrieving data from request
        # get_data = request.get_json()

        # checking if item already exists
        item = next(filter(lambda x: x['name'] == name, items), None)
        # if exists => update
        if item:
            item.update(args)
            return item, 201
        # create
        else:
            item = self.post(name)
            return item


# somehow creates an entry point
api.add_resource(Item, '/item/<string:name>')


# this class is used to list all items
class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(ItemList, '/item')

app.run(debug=True, port=5000)
