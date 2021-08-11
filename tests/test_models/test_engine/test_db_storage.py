#!/usr/bin/python3
""" Module for testing db storage"""
import unittest
from models.base_model import Base
from models.state import State
from models.engine.db_storage import DBStorage
from models import storage
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
        """ Set up each test case """
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            self.skipTest('Using File Storage')
        else:
            self.db = MySQLdb.connect(host=self.host, port=3306,
                                      db=self.dbname, charset="utf8",
                                      user=self.user, passwd=self.pwd)
        self.cur = self.db.cursor()

    def tearDown(self):
        self.cur.execute("""DELETE FROM states;""")
        self.cur.close()
        self.db.close()

    def test_new_save(self):
        """ New object is correctly added to database """
        self.cur.execute("SELECT COUNT(*) FROM states;")
        init_count = self.cur.fetchall()[0][0]
        self.cur.close()
        self.db.close()

        state = State(name="California")
        state.save()

        self.db = MySQLdb.connect(host=self.host, port=3306,
                                  db=self.dbname, charset="utf8",
                                  user=self.user, passwd=self.pwd)
        self.cur = self.db.cursor()
        self.cur.execute("SELECT COUNT(*) FROM states;")
        final_count = self.cur.fetchall()[0][0]

        self.assertNotEqual(init_count, final_count)

    def test_all(self):
        """ All query is done correctly """
        state = State(name="California")
        state.save()

        query_dict = storage.all('State')

        self.cur = self.db.cursor()
        self.cur.execute("SELECT * FROM states;")
        query = self.cur.fetchall()[0]

        attrs = ['id', 'created_at', 'updated_at', 'name']
        for idx, attr in enumerate(attrs):
            if (attr in ['created_at', 'updated_at']):
                self.assertEqual(list(query_dict.values())[0].
                                 __dict__[attr].isoformat().split('.')[0][:-3],
                                 query[idx].isoformat()[:-3])
            else:
                self.assertEqual(list(query_dict.values())[0].__dict__[attr],
                                 query[idx])

    def test_delete():
        """Delete query is done correctly"""
        pass


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
