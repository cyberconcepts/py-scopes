# scopes.tests.test_standard

"""Tests for the 'scopes.storage' package."""

import os, sys
sys.path = [os.path.dirname(__file__)] + sys.path

import unittest
from scopes.tests import tlib_web, tlib_storage

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

    def test_013_web(self):
        tlib_web.test_app(self, config)
        tlib_web.test_auth(self, config)
        tlib_web.test_user_data(self, config)


def suite():
    return unittest.TestSuite((
        unittest.TestLoader().loadTestsFromTestCase(Test),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
