from flask_restful import Resource, reqparse
from store_model.store_model import StoreModel


class Store(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('store_name',
                        type=str,
                        required=False)
    parser.add_argument('store_id',
                        type=int,
                        required=False)
    parser.add_argument('new_store_name',
                        type=str,
                        required=False)

    def get(self):
        args = Store.parser.parse_args()
        store_name = args.get('store_name', None)
        store_id = args.get('store_id', None)
        if store_id and store_name:
            result = StoreModel.get_store_by_id(store_id=store_id)
            return StoreModel.store_to_json(), 200
        elif not store_name and store_id:
            result = StoreModel.get_store_by_id(store_id=store_id)
            return result.store_to_json(), 200
        elif store_name and not store_id:
            result = StoreModel.get_from_db(store_name=store_name)
            return result.store_to_json(), 200
        else:
            list_of_storeModels = StoreModel.get_all_stores()
            if list_of_storeModels:
                list_of_store_json = list(map(lambda x: x.store_to_json(), list_of_storeModels))
                return {'stores': list_of_store_json}, 200
            else:
                return {"message": "no stores found in the database"}, 404
    def post(self):
        args = Store.parser.parse_args()
        store_name = args.get('store_name', None)
        if not store_name:
            return {"message": "store_name is required"}, 401
        elif store_name:
            my_store_in_db = StoreModel.get_from_db(store_name)
            if my_store_in_db:
                return {"message": f"a store named {store_name} already exists"}, 401
            else:
                store = StoreModel(name=store_name)
                store.set_in_db()
                return store.store_to_json(), 201

    def put(self):
        args = Store.parser.parse_args()
        store_name = args.get('store_name', None)
        new_store_name = args.get('new_store_name', None)
        if not store_name or not new_store_name:
            return {"message": "store_name is required"}, 401
        elif store_name and new_store_name:
            store = StoreModel(name=store_name)
            store.update_store(new_store_name)
            return store.store_to_json(), 201

    # in know this function is over-sized but,
    # i like my functions like I like my girls
    # thick.
    def delete(self):
        args = Store.parser.parse_args()
        store_name = args.get('store_name', None)
        store_id = args.get('store_id', None)
        if store_id:
            store = StoreModel.get_store_by_id(store_id)
            if store:
                store.delete_from_db()
                return {"message": f"store with id {store_id} was deleted from the database"}.update(store.store_to_json()), 201
            elif store_name:
                store = StoreModel.get_from_db(store_name)
                if store:
                    store.delete_from_db()
                    return {"message": "store deleted"}.update(store.store_to_json()), 201
        elif store_name:
            store = StoreModel.get_from_db(store_name)
            if store:
                store.delete_from_db()
                message = {"message": "store deleted"}
                message.update(store.store_to_json())
                return message, 201
            else:
                return {"message": f"no store named {store_name} was found in the database"}, 404
        else:
            return {"message": f"no store was deleted, try entering a valid store_name or store_id."}, 404