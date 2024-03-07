#! /usr/bin/python

"""Tests for the 'scopes.storage' package."""

import config

from datetime import datetime
import unittest

import scopes.storage.common
from scopes.storage.common import commit, Storage, getEngine, sessionFactory
#from scopes.storage import proxy
from scopes.storage import folder, tracking

engine = getEngine(config.dbengine, config.dbname, config.dbuser, config.dbpassword) 
scopes.storage.common.engine = engine
scopes.storage.common.Session = sessionFactory(engine)

storage = Storage(schema=config.dbschema)

import tlib

class Test(unittest.TestCase):
    "Basic tests for the cco.storage package."

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
