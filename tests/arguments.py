#!/usr/bin/env python3
"""
Testing module console.
"""

import unittest
from templateme.arguments import Argument


# This is tested class. Can have too many method
class TestArgumentsModule(unittest.TestCase):  # pylint: disable=R0904
    """ Module testsCase. """

    def test_argument(self):
        """ Tests if Argument object work good. """
        first_argument = Argument("first_Argument")
        first_argument.value = "first_Value"
        self.assertEqual(first_argument.value, "first_Value")
        self.assertEqual(first_argument.name, "FIRST_ARGUMENT")
        first_argument.value = "second Value"
        self.assertEqual(first_argument.value, "second Value")

    def test_argument_require(self):
        """ Tests if require mechanism works good. """
        default_arg = Argument("element")
        self.assertEqual(default_arg.is_set, False)
        default_arg.value = "test"
        self.assertEqual(default_arg.is_set, True)

        default_arg = Argument("element", required=False)
        self.assertEqual(default_arg.is_set, True)
        default_arg.value = "test"
        self.assertEqual(default_arg.is_set, True)

        default_arg = Argument("element", default="test")
        self.assertEqual(default_arg.value, "test")
        self.assertEqual(default_arg.is_set, False)
        default_arg.value = "test2"
        self.assertEqual(default_arg.value, "test2")
        self.assertEqual(default_arg.is_set, True)


if __name__ == "__main__":
    unittest.main()
