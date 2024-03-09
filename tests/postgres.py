#! /usr/bin/python

"""Tests for the 'scopes.storage' package - using PostgreSQL."""

import unittest

import config
config.dbengine = 'postgresql+psycopg'
config.dbname = 'testdb'
config.dbuser = 'testuser'
config.dbpassword = 'secret'
config.dbschema = 'testing'

# PostgreSQL-specific settings
from scopes.storage.db import postgres 
postgres.init()

import tlib
tlib.init(config)
#factory = postgres.StorageFactory(config)
#storage = factory(schema='testing')

class Test(unittest.TestCase):

    def test_001_tracking(self):
        tlib.test_tracking(self)

    def test_002_folder(self):
        tlib.test_folder(self)

def suite():
    return unittest.TestSuite((
        unittest.TestLoader().loadTestsFromTestCase(Test),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
