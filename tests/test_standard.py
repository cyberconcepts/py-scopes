#! /usr/bin/python

"""Tests for the 'scopes.storage' package."""

import unittest

import config
import tlib
tlib.init(config)
#from scopes.storage.common import StorageFactory
#factory = StorageFactory(config)
#storage = factory(schema=None)

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
