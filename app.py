# noinspection SpellCheckingInspection
stores = [
    {
        'store': 'qadia_annaba',
        'items': [
            {
                'name': 'olive_oil',
                'price': 500,
            },
            {
                'name': 'milk',
                'price': 100,
            },
        ],
    },
    {
        'store': 'qadia_alger',
        'items': [
            {
                'name': 'eggs',
                'price': 10,
            },
            {
                'name': 'cheese',
                'price': 50,
            }
        ]
    }
]



from flask import Flask, jsonify, request

app = Flask(__name__)


# this just a place holder for the index
@app.route('/')
def main_route():
    return 'Main Page Here'


# POST this function creates a store
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_data = {
        'store': request_data['store'],
        'items': request_data['items']
    }
    stores.append(new_data)
    return jsonify(new_data)


# POST specific item
@app.route('/store/<string:name>/item', methods=['POST'])
def post_item(name):
    request_data = request.get_json()
    for store in stores:
        if name == store['store']:
            new_data = {
                'name': request_data['name'],
                'price': request_data['price'],
            }
            store['items'].append(new_data)
            return jsonify(store)
    return 'No such store was found'


# GET this allows for getting a specific store
@app.route('/store/<string:name>', methods=['GET'])
def get_specific_store(name):
    for store in stores:
        if name == store['store']:
            return jsonify(store)
    return 'Error: no such store was found.'


# GET item from store
@app.route('/store/<string:name>/items', methods=['GET'])
def get_items(name):
    for store in stores:
        if name == store['store']:
            return jsonify({'items': store['items']})
    return 'No such store was found'


# GET all stores
@app.route('/store', methods=['GET'])
def get_all_store():
    hwanet = stores
    return jsonify({'list_of_stores': hwanet})


app.run(port=5000, debug=True)


