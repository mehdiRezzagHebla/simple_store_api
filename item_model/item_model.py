import os
from db import dbalch

db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'first_db.db')

# this son of a bitch better be working from test 01
# this a bad son of a b****, ofc he will
# MRH :~


class ItemModel(dbalch.Model):

    __tablename__ = 'items'

    id = dbalch.Column(dbalch.Integer, primary_key=True)
    name = dbalch.Column(dbalch.String(256))
    price = dbalch.Column(dbalch.Float(precision=2))

    # this gives us access to the id of the store in another table (stores)
    store_id = dbalch.Column(dbalch.Integer, dbalch.ForeignKey('stores.id'))
    # this one links the two together
    # TODO: investigate this a bit further to see how it works internally
    # hypothesis: this maybe allows for backward refrencing, in order to find which store the item belongs to?
    # this is probably it, because the ForeignKey allows only for retrieving the id number
    # whereas this one (relationship) allows for retrieving the instance (ex. store 1) to which the item belongs to.
    # having set .relationsip() in both StoreModel and ItemModel allows for
    # asserting that this is a one-to-many relationship
    store = dbalch.relationship('StoreModel')

    def __init__(self, id, name, price, store_id):
        self.id = id
        self.name = name
        self.price = price
        self.store_id = store_id

    # this transforms ItemModel object to a json/dict format
    def item_to_json(self):
        return {'name': self.name, 'price': self.price, 'store_id': self.store_id}

    @classmethod
    def to_item_model(cls, json):
        # TODO: check again if should include _id
        return cls(name=json['name'], price=json['price'], id=json['id'], store_id=json['store_id'])

    # if item exists returns an ItemModel object
    # else returns None
    @classmethod
    def get_from_db(cls, item_name):
        result = cls.query.filter_by(name=item_name).first()
        return result

        '''
        db = sqlite3.connect(db_path, check_same_thread=False)
        cursor = db.cursor()

        get_item_query = 'SELECT * FROM items WHERE name = ?'
        result = cursor.execute(get_item_query, (item_name,)).fetchone()
        db.close()
        # if item exists
        if result:
            return cls(name=result[1], price=result[2], id=[0])
        else:
            return None
        '''
    # inserts & updates
    def set_in_db(self):
        dbalch.session.add(self)
        dbalch.session.commit()

    def delete_from_db(self):
        dbalch.session.delete(self)
        dbalch.session.commit()
    '''# puts/updates item in db
    def set_in_db(self, force=False):
        # TODO: take print statement off
        print(f">>>>\n{db_path}\n>>>>")
        db = sqlite3.connect(db_path, check_same_thread=False)
        cursor = db.cursor()

        # check if item exists first
        item_from_db = self.get_from_db(self.name)
        # if item exists and force update is True, then update
        # and return ItemModel
        if item_from_db and force:
            update_item_query = 'UPDATE items SET price = ? WHERE name = ?'
            cursor.execute(update_item_query, (self.price, self.name))
            db.commit()
            updated_item_from_db = self.get_from_db(self.name)
            db.close()
            return updated_item_from_db
        # if item exists but force is False
        # just return the item from db without updating
        elif item_from_db and not force:
            db.close()
            return item_from_db
        # if item doesn't exist
        # create
        else:
            create_item_query = 'INSERT INTO items (name, price) VALUES (?, ?)'
            cursor.execute(create_item_query, (self.name, self.price))
            db.commit()
            item_from_db = self.get_from_db(self.name)
            db.close()
            return item_from_db
        '''
    # deletes
    # I mean... It's obvious
