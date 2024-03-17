# scopes/tests.py

"""The real test implementations"""

import unittest
from scopes import tlib_storage

import config
config.dbengine = 'postgresql'
config.dbname = 'ccotest'
config.dbuser = 'ccotest'
config.dbpassword = 'cco'
config.dbschema = 'testing'

# PostgreSQL-specific settings
from scopes.storage.db.postgres import StorageFactory 
config.storageFactory = StorageFactory(config)
#storage = factory(schema='testing')


class Test(unittest.TestCase):

    def test_001_tracking(self):
        tlib_storage.test_tracking(self, config)
   
    def test_002_folder(self):
        tlib_storage.test_folder(self, config)
   
    def test_003_type(self):
        tlib_storage.test_type(self, config)
   
    def test_004_topic(self):
        tlib_storage.test_topic(self, config)
