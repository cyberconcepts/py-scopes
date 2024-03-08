#! /usr/bin/python

"""Tests for the 'scopes.storage' package."""

from datetime import datetime
import unittest

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
