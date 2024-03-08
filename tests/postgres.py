#! /usr/bin/python

"""Tests for the 'scopes.storage' package - using PostgreSQL."""

from datetime import datetime
import unittest

# PostgreSQL-specific settings
import scopes.storage.db.postgres
import config
config.dbengine = 'postgresql+psycopg'
config.dbname = 'testdb'
config.dbuser = 'testuser'
config.dbpassword = 'secret'
config.dbschema = 'testing'

import tlib

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
