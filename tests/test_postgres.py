#! /usr/bin/python

"""Tests for the 'scopes.storage' package - using PostgreSQL."""

import unittest
import tlib_storage

from scopes.storage.db.postgres import StorageFactory 
import config
config.dbengine = 'postgresql+psycopg'
config.dbname = 'testdb'
config.dbuser = 'testuser'
config.dbpassword = 'secret'
config.dbschema = 'testing'
config.storageFactory = StorageFactory(config)


class Test(unittest.TestCase):

    def test_001_tracking(self):
        tlib_storage.test_tracking(self, config)

    def test_002_folder(self):
        tlib_storage.test_folder(self, config)

def suite():
    return unittest.TestSuite((
        unittest.TestLoader().loadTestsFromTestCase(Test),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
