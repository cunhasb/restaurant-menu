# import sys
# import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import pdb


class RestaurantCrud(object):
    engine = create_engine('sqlite:///restaurantmenu.db')

    def __init__(self, name=None, id=None):
        self.name = name
        self.id = id
        Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def create(self):
        restaurant = Restaurant(name=self.name)
        # pdb.set_trace()
        self.session.add(restaurant)
        self.session.commit()
        return restaurant

    def read(self):
        return self.session.query(Restaurant)

    def find(self):
        return self.session.query(Restaurant).filter_by(id=self.id).one()

    def update(self, new_name):
        restaurant = self.session.query(Restaurant).filter_by(id=self.id).one()
        restaurant.name = new_name
        # pdb.set_trace()
        self.session.add(restaurant)
        self.session.commit()
        return restaurant

    def delete(self):
        restaurant = self.session.query(Restaurant).filter_by(id=self.id).one()
        # pdb.set_trace()
        self.session.delete(restaurant)
        self.session.commit()
        return 'Restaurant deleted!'
