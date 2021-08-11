#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.user import User


class test_User(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

        self.obj = self.value(first_name="John",
                              last_name="Doe",
                              email="john.doe@johndoe.com",
                              password="johndoe123")

    def test_first_name(self):
        """ """
        self.assertEqual(type(self.obj.first_name), str)

    def test_last_name(self):
        """ """
        self.assertEqual(type(self.obj.last_name), str)

    def test_email(self):
        """ """
        self.assertEqual(type(self.obj.email), str)

    def test_password(self):
        """ """
        self.assertEqual(type(self.obj.password), str)
