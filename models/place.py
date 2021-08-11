#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey


association_table = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60), ForeignKey(
                              'places.id'), nullable=False),
                          Column('amenity_id', String(60), ForeignKey(
                              'amenities.id'), nullable=False)


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

    if models.env == 'db':
        reviews = relationship("Review", cascade="delete", backref="place")
        amenities = relationship("Amenity",
                                 secondary=association_table,
                                 viewonly=False)                                               )
    else:
        @property
        def reviews(self):
            review_dict = models.storage.all(Review)
            review_list = []
            for key, val in review_dict.items():
                if val.place_id == self.id:
                    review_list.append(val)
            return review_list

