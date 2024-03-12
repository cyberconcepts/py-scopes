#! /usr/bin/python

"""Tests for the 'scopes.storage' package."""

import unittest
import tlib_storage

from scopes.storage.common import StorageFactory
import config
config.dbengine = 'sqlite'
config.dbname = 'var/test.db'
config.dbschema = None
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
