#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state",
                          cascade="delete")

    @property
    def cities(self):
        city_dict = models.storage.all(City)
        city_list = []
        for key, val in city_dict.items():
            if val.state_id == self.id:
                city_list.append(val)
        return city_list
