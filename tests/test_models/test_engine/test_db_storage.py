#!/usr/bin/python3
""" Module for testing db storage"""
import unittest
from models.state import State
from models.engine.db_storage import DBStorage
from models.__init__ import storage
import os
import inspect
import pep8
import MySQLdb


class test_DBStorage(unittest.TestCase):
    """ Class to test the db storage method """

    @classmethod
    def setUpClass(cls):
        """ Set up test environment """
        cls.user = os.getenv('HBNB_MYSQL_USER')
        cls.pwd = os.getenv('HBNB_MYSQL_PWD')
        cls.host = os.getenv('HBNB_MYSQL_HOST')
        cls.dbname = os.getenv('HBNB_MYSQL_DB')

    def setUp(self):
        self.db = MySQLdb.connect(host=self.host, port=3306,
                                  db=self.dbname, charset="utf8",
                                  user=self.user, passwd=self.pwd)

    def tearDown(self):
        self.db.close()

    def test_new(self):
        """ New object is correctly added to database """
        cur = self.db.cursor()
        cur.execute("SELECT COUNT(*) FROM states;")
        init_count = cur.fetchall()[0][0]
        cur.close()
        self.db.close()

        state = State(name="California")
        state.save()

        self.db = MySQLdb.connect(host=self.host, port=3306,
                                  db=self.dbname, charset="utf8",
                                  user=self.user, passwd=self.pwd)
        cur = self.db.cursor()
        cur.execute("SELECT COUNT(*) FROM states;")
        final_count = cur.fetchall()[0][0]
        cur.close()

        self.assertNotEqual(init_count, final_count)


class TestDBStorageDoc(unittest.TestCase):
    "Tests documentation and pep8 for DBStorage class."

    @classmethod
    def setUpClass(cls):
        """Sets the whole functions of the class DBStorage to be inspected for
        correct documentation."""
        cls.functions = inspect.getmembers(DBStorage,
                                           inspect.isfunction(DBStorage))

    def test_doc_module(self):
        """Tests for docstring presence in the module and the class."""
        from models.engine import db_storage

        self.assertTrue(len(db_storage.__doc__) > 0)
        self.assertTrue(len(db_storage.DBStorage.__doc__) > 0)

    def test_doc_fun(self):
        """Tests for docstring presence in all functions of class."""
        for fun in self.functions:
            self.assertTrue(len(fun.__doc__) > 0)

    def test_pep8(self):
        """Tests pep8 style compliance of module and test files."""
        p8 = pep8.StyleGuide(quiet=False)

        res = p8.check_files(['models/engine/db_storage.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")
        res = p8.check_files(
            ['tests/test_models/test_engine/test_db_storage.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")
