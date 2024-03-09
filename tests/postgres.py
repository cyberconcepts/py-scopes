#! /usr/bin/python

"""Tests for the 'scopes.storage' package - using PostgreSQL."""

import unittest

import config
config.dbengine = 'postgresql+psycopg'
config.dbname = 'testdb'
config.dbuser = 'testuser'
config.dbpassword = 'secret'

# PostgreSQL-specific settings
from scopes.storage.db.postgres import StorageFactory 
factory = StorageFactory(config)
storage = factory(schema='testing')

import tlib

class Test(unittest.TestCase):

    def test_001_tracking(self):
        tlib.test_tracking(self, storage)

    def test_002_folder(self):
        tlib.test_folder(self, storage)

def suite():
    return unittest.TestSuite((
        unittest.TestLoader().loadTestsFromTestCase(Test),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
