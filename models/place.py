#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table
from sqlalchemy.orm import relationship
import models


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)

    association_table = Table('place_amenity', Base.metadata,
                              Column('place_id', String(60),
                                     ForeignKey('places.id'),
                                     nullable=False),
                              Column('amenity_id', String(60),
                                     ForeignKey('amenities.id'),
                                     nullable=False))

    if models.env == 'db':
        reviews = relationship("Review", backref="place",
                               cascade="all, delete-orphan")
        amenities = relationship("Amenity",
                                 secondary=association_table,
                                 viewonly=False)
    else:
        amenity_ids = []

        @property
        def reviews(self):
            """ Returns the list of reviews for the current place """
            review_dict = models.storage.all(Review)
            review_list = []
            for key, val in review_dict.items():
                if val.place_id == self.id:
                    review_list.append(val)
            return review_list

        @property
        def amenities(self):
            """ Returns the list of amenity ids stored """
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj):
            """ Pushes a new amenity id to the list """
            if isinstance(obj, Amenity):
                self.amenity_ids.push(obj.id)
