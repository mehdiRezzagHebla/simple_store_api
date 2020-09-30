from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
import os
from item_model.item_model import ItemModel


# MRH :~
# this module is the resource that converses with the client
# it provides the client with CRUD operations
# this module uses the model to shape the data (ItemModel class)


# the Resource inheritance allows for handling the conversion dict-json I guess
# also Resource allows for specifying the HTTP verb just by overwriting get/post/delete, etc.
# this class is used to create an item and to retrieve an item
class Item(Resource):



    # my queries
    query_get_name = 'SELECT * FROM items WHERE name=?'
    query_post = 'INSERT INTO items (name, price) VALUES (?, ?)'
    # delete in case there is a limit
    query_delete_name_limit = 'DELETE FROM items WHERE name = (SELECT name FROM items WHERE name = ? LIMIT {lim})'
    # update tuple (new_name, old_name)
    query_put_name = 'UPDATE items SET name = :new_name WHERE name = old_name'
    query_put_price = 'UPDATE items SET price = :new_price WHERE price = :old_price'
    query_put_name_and_price = """UPDATE items SET name = :new_name, price = :new_price WHERE name = :old_name AND price = :old_price"""

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

    # this parser is just for the put method (endpoint
    parser.add_argument('old_name',
                        type=str,
                        required=False,)
    parser.add_argument('old_price',
                        type=float,
                        required=False)
    parser.add_argument('new_name',
                        type=str,
                        required=False)
    parser.add_argument('new_price',
                        type=float,
                        required=False)
    # the below parser is just in case we want to update the price but NOT name
    # to avoid using inaccurate terminology (old_name or new_name)
    parser.add_argument('name',
                        type=str,
                        required=False)
    parser.add_argument('delete_limit',
                        type=int,
                        required=False)
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Store_id is required.')

    @jwt_required()
    def get(self, name):
        result = ItemModel.get_from_db(name)
        if not result:
            return {'message': f'no item named {name} was found in the database.'}, 404
        else:
            return result.item_to_json(), 200

    def post(self, name):
        args = Item.parser.parse_args()
        item = ItemModel.get_from_db(name)
        if item:
            item.price = args['price']
            item.store = args['store_id']
            return {"message": "Item already exists and has been changed."}.update(item.item_to_json()), 201
        else:
            item = ItemModel(name=name,price=args['price'], id=None, store_id=args['store_id'])
            item.set_in_db()
            return item.item_to_json(), 201

    def delete(self, name):
        item = ItemModel.get_from_db(name)
        if item:
            item.delete_from_db()
            return {"message": "item deleted", "item": item.item_to_json()}
        else:
            return {"message": f"Item named {name} not found"}, 404
    '''
    def delete(self, name):
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'first_db.db')
        db = sqlite3.connect(db_path, check_same_thread=False)
        cursor = db.cursor()
        args = Item.parser.parse_args()
        limit = args.get('delete_limit', 0)
        if not limit:
            limit = 0
        # TODO: take off print statements
        print(limit, type(limit))
        items = cursor.execute(Item.query_get_name, (name,)).fetchall()
        # if the list of to-be-deleted items is empty
        if not items:
            return {"message": f"No item named {name} was found"}, 404
        # if to-be-deleted item exists
        else:
            new_query = Item.query_delete_name_limit.format(lim=limit)
            print(new_query)
            cursor.execute(new_query, (name,))
            db.commit()
            db.close()
            returned_list_of_dicts = []
            for row in items:
                single_dict = {
                    "name": row[1],
                    "price": row[2]
                }
                returned_list_of_dicts.append(single_dict)
            return {"items deleted": returned_list_of_dicts}, 201'''

    def put(self, name):
        args = Item.parser.parse_args()
        item = ItemModel(name=name, price=args['price'], id=None, store_id=args['store_id'])
        item.set_in_db()
        return item.item_to_json(), 201

        '''        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'first_db.db')
        db = sqlite3.connect(db_path, check_same_thread=False)
        cursor = db.cursor()
        # this replaces the request.get_json()
        # and returns only the arguments provided in add_argument
        args = Item.parser.parse_args()
        change_both_dict = {
            'old_name': args.get('old_name', None),
            'old_price': args.get('old_price', None),
            'new_name': args.get('new_name', None),
            'new_price': args.get('new_price', None),
            'name': args.get('name', None)
        }
        # change both
        if change_both_dict['old_name'] and change_both_dict['old_price'] and change_both_dict['new_name'] and change_both_dict['new_price']:
            cursor.execute(Item.query_get_name, (change_both_dict['old_name'],))
            if cursor.fetchone():
                cursor.execute(Item.query_put_name_and_price, change_both_dict)
                db.commit()
                returned_val = cursor.execute(Item.query_get_name, (change_both_dict['new_name'],)).fetchone()
                returned_dict = {'name': returned_val[1], 'price': returned_val[2]}
                db.close()
                return returned_dict, 201
            else:
                cursor.execute(Item.query_post, (change_both_dict['new_name'], change_both_dict['new_price']))
                db.commit()
                returned_val = cursor.execute(Item.query_get_name, (change_both_dict['new_name'],)).fetchone()
                returned_dict = {'name': returned_val[1], 'price': returned_val[2]}
                db.close()
                return returned_dict, 201
        # change name only
        elif change_both_dict['old_name'] and not change_both_dict['old_price'] and change_both_dict['new_name'] and not change_both_dict['new_price']:
            cursor.execute(Item.query_get_name, (change_both_dict['old_name'],))
            if cursor.fetchone():
                cursor.execute(Item.query_put_name, change_both_dict)
                db.commit()
                returned_val = cursor.execute(Item.query_get_name, (change_both_dict['old_name'],)).fetchone()
                returned_dict = {'name': returned_val[1], 'price': returned_val[2]}
                db.close()
                return returned_dict, 201
            else:
                # can't create entry because no price; return not found message instead
                return {'message': f'no such item named {change_both_dict["old_name"]}'}, 400
        # change price only
        elif change_both_dict['name'] and change_both_dict['old_price'] and change_both_dict['new_price'] and not change_both_dict['new_name'] and not change_both_dict['old_name']:
            cursor.execute(Item.query_get_name, (change_both_dict['name'],))
            if cursor.fetchone():
                cursor.execute(Item.query_put_price, {'old_price':change_both_dict['old_price'], 'new_price': change_both_dict['new_price']})
                db.commit()
                returned_val = cursor.execute(Item.query_get_name, (change_both_dict['name'],)).fetchone()
                returned_dict = {'name': returned_val[1], 'price': returned_val[2]}
                db.close()
                return returned_dict, 201
            else:
                cursor.execute(Item.query_post, (change_both_dict['name'], change_both_dict['new_price']))
                db.commit()
                returned_val = cursor.execute(Item.query_get_name, (change_both_dict['name'],)).fetchone()
                returned_dict = {'name': returned_val[1], 'price': returned_val[2]}
                db.close()
                copy_with = {'message': f'no such item named {change_both_dict["name"]}, created a new entry.'}
                return returned_dict.update(copy_with), 201
        # in case everything else fails
        else:
            return {'message': 'Error happened, investigate json content or Item API put method'}, 400
'''

# this class is used to list all items
class ItemList(Resource):

    def get(self):
        all_items = ItemModel.query.all()
        list_of_item_json = []
        if all_items:
            for item in all_items:
                print(item, type(item))
                print(item.item_to_json())
                list_of_item_json.append(item.item_to_json())
            return {"list of all items": list_of_item_json}, 200
        else:
            return {"message": "no items could be found in the database"}, 404