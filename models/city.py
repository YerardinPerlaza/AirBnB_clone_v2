#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"

    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
<<<<<<< HEAD
    places = relationship("Place", backref="cities",
                          cascade="delete")
=======
>>>>>>> adb4e1c490ed49228fb35d8d76cb16f29f490855
