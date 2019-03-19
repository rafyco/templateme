#!/usr/bin/env python3
"""
Testing module templates.
"""

import unittest


# This is tested class. Can have too many method
class TestTemplatesModule(unittest.TestCase):  # pylint: disable=R0904
    """ Module testsCase. """

    def test_example(self):
        """ Test invalid arguments. """
        self.assertEqual("", "")

if __name__ == "__main__":
    unittest.main()
