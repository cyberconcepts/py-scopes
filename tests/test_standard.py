#! /usr/bin/python

"""Tests for the 'scopes.storage' package."""

import unittest
import tlib_server, tlib_storage

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

    def test_003_type(self):
        tlib_storage.test_type(self, config)

    def test_004_topic(self):
        tlib_storage.test_topic(self, config)

    def test_013_server(self):
        tlib_server.test_app(self, config)


def suite():
    return unittest.TestSuite((
        unittest.TestLoader().loadTestsFromTestCase(Test),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
