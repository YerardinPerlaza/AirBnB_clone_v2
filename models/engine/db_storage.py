#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """Documentation"""
    __engine = None
    __session = None

    def __init__(self):
        """Documentation"""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.
                                      format(user, pwd, host, db),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all()

    def all(self, cls=None):
        """Documentation"""
        classes = {
            'User': User, 'Place': Place,
            'State': State,
            'City': City  # 'Amenity': Amenity, 'Review': Review
        }
        q_dict = {}

        if cls:
            for obj in self.__session.query(classes[cls]).all():
                q_dict[cls + '.' + obj.id] = obj
        else:
            for cls_name, cls_val in classes.items():
                for obj in self.__session.query(cls_val).all():
                    q_dict[cls_name + '.' + obj.id] = obj

        self.reload()
        return q_dict

    def new(self, obj):
        """Documentation"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Documentation"""
        self.__session.commit()

    def delete(self, obj=None):
        """Documentation"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Documentation"""
        Base.metadata.create_all(self.__engine)

        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()
