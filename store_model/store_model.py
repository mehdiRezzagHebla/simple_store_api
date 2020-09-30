import os
from db import dbalch

db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'first_db.db')

# this son of a bitch better be working from test 01
# this a bad son of a b****, ofc he will
# MRH :~


class StoreModel(dbalch.Model):

    __tablename__ = 'stores'

    id = dbalch.Column(dbalch.Integer, primary_key=True)
    name = dbalch.Column(dbalch.String(256))

    # see comments in the ItemModel class for more clarification
    items = dbalch.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name,):
        self.name = name

    # this transforms ItemModel object to a json/dict format
    def store_to_json(self):
        return {'name': self.name, 'items': list(map(lambda x: x.item_to_json(), self.items.all()))}

    # transform from json to StoreModel object
    @classmethod
    def to_store_model(cls, json):
        # TODO: check again if should include _id
        return cls(name=json['name'])

    # if item exists returns an ItemModel object
    # else returns None
    @classmethod
    def get_from_db(cls, store_name):
        result = cls.query.filter_by(name=store_name).first()
        return result

    @classmethod
    def get_store_by_id(cls, store_id):
        result = cls.query.filter_by(id=store_id).first()
        return result

    @classmethod
    def get_all_stores(cls):
        result = cls.query.order_by(cls.id).all()
        return result

    # inserts & updates
    def set_in_db(self):
        dbalch.session.add(self)
        dbalch.session.commit()

    # inserts & updates
    def update_store(self, new_name):
        self.name = new_name
        dbalch.session.add(self)
        dbalch.session.commit()

    def delete_from_db(self):
        dbalch.session.delete(self)
        dbalch.session.commit()

    # deletes
    # I mean... It's obvious
