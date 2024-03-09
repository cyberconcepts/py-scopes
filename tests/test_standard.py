#! /usr/bin/python

"""Tests for the 'scopes.storage' package."""

import unittest

import config
config.dbengine = 'sqlite'
config.dbname = 'var/test.db'

from scopes.storage.common import StorageFactory
factory = StorageFactory(config)
storage = factory(schema=None)

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
