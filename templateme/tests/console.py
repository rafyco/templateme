#!/usr/bin/env python3
"""
Testing module console.
"""

from __future__ import unicode_literals
import unittest
import sys
from io import StringIO
import mock
import templateme
from templateme.console import main as console_program


# This is tested class. Can have too many method
class TestConsoleModule(unittest.TestCase):  # pylint: disable=R0904
    """ Module testsCase. """

    def setUp(self):
        """ Setup environment. """
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        sys.stdout = self.tmp_stdout = StringIO()
        sys.stderr = StringIO()

    def tearDown(self):
        """ Teardown environment. """
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

    def test_console(self):
        """ Test that console app work ok. """
        status = 0
        try:
            console_program(["--help"])
        except SystemExit as ex:
            if ex.code is not None:
                status = ex.code  # pylint disable=E0012,R0204
        self.assertEqual(status, 0)
        self.assertNotEqual(self.tmp_stdout.getvalue(), "")

    def test_invalid_args(self):
        """ Test invalid arguments. """
        status = 0
        try:
            console_program(["--invalid-arg", "--another-invalid-arg"])
        except SystemExit as ex:
            if ex.code is not None:
                status = ex.code  # pylint disable=E0012,R0204
        self.assertEqual(self.tmp_stdout.getvalue(), "")
        self.assertNotEqual(status, 0)

    def test_version(self):
        """ Test invalid arguments. """
        status = 0
        try:
            console_program(["--version"])
        except SystemExit as ex:
            if ex.code is not None:
                status = ex.code  # pylint disable=E0012,R0204
        self.assertEqual(status, 0)
        self.assertEqual(self.tmp_stdout.getvalue().strip(),
                         "templateme {}".format(templateme.get_version()))

    def test_listing(self):
        """ Testing list of default templates. """
        status = 0
        try:
            console_program(['--list'])
        except SystemExit as ex:
            if ex.code is not None:
                status = ex.code  # pylint disable=E0012, R0204
        self.assertEqual(status, 0)

    def test_create_template(self):
        """ Test if template works. """
        str_check = 'SomeStringTakePlaceInCode'
        status = 0
        try:
            with mock.patch('builtins.input', return_value=str_check):
                console_program(['-t', 'cpp'], debug=True)
        except SystemExit as ex:
            if ex.code is not None:
                status = ex.code  # pylint disable=E0012, R0204
        self.assertEqual(status, 0)
        self.assertTrue(self.tmp_stdout.getvalue().find(str_check) > -1)

    def test_create_with_arguments(self):
        """ Test if argument arg works. """
        str_check = 'SomeStringTakePlaceInCode'
        status = 0
        try:
            console_program(['-t', 'cpp', '-a', "class={}".format(str_check)], debug=True)
        except SystemExit as ex:
            if ex.code is not None:
                status = ex.code  # pylint disable=E0012, R0204
        self.assertEqual(status, 0)
        self.assertTrue(self.tmp_stdout.getvalue().find(str_check) > -1)

        for invalid_arg in ["value", "=", "a=", "=a", "a=a=v"]:
            try:
                console_program(['-t', 'cpp', '-a', "class=class",
                                 '-a', invalid_arg],
                                debug=True)
            except SystemExit as ex:
                if ex.code is not None:
                    status = ex.code  # pylint disable=E0012, R0204
            self.assertEqual(status, 2, "Invalid argument test result:({}=2), checked arg [{}]"
                             "".format(status, invalid_arg))

    def test_create_template_quiet(self):
        """ Test if template realy not ask in quiet mode. """
        status = 0
        try:
            console_program(['-t', 'cpp', '-q'], debug=True)
        except SystemExit as ex:
            if ex.code is not None:
                status = ex.code  # pylint disable=E0012, R0204
        self.assertEqual(status, 2)


if __name__ == "__main__":
    unittest.main()
