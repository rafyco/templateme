#!/usr/bin/env python3
"""
Testing module templateme.

TestCase checking module files. It should be conform to PEP8.

@see: L{templateme}
"""

from __future__ import unicode_literals
import unittest
import os
import sys
from io import StringIO
import pep8
from pylint.lint import Run as run_pylint
import templateme


# This is tested class. Can have too many method
class TestTemplateMeModule(unittest.TestCase):  # pylint: disable=R0904
    """ Module testsCase. """
    @staticmethod
    def __get_sources_file():
        """ Get all paths to source files in templateme module. """

        def recursive_checker(main_directory):
            """ Recursive function to find all source file in direcotry. """
            result = []
            for source_file in os.listdir(main_directory):
                if (source_file.endswith(".py") and
                        os.path.isfile(os.path.join(main_directory,
                                                    source_file))):
                    result.append(os.path.join(main_directory, source_file))
                elif source_file == "templates":
                    continue
                elif os.path.isdir(os.path.join(main_directory, source_file)):
                    result = (result +
                              recursive_checker(os.path.join(main_directory,
                                                             source_file)))
            return result
        return recursive_checker(templateme.__path__[0])

    def test_pep8(self):
        """ Tests that we conform to PEP8. """
        pep8_style = pep8.StyleGuide(paths=['--ignore=E501'])
        # Disable E501 code (line too long). It should be enabled after fixed.
        result = pep8_style.check_files(TestTemplateMeModule.__get_sources_file())
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pylint(self):
        """ Tests that we conform to Pylint's rules. """
        status = 0
        output = None
        try:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = output = StringIO()
            sys.stderr = StringIO()
            run_pylint(['-d', 'I0011,R0801,R0902,R0903,R0913,R0921', 'templateme'])
        except SystemExit as ex:
            status = int(ex.code)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        if status != 0 and output is not None:
            print(output.getvalue())
        self.assertEqual(status, 0, "[Pylint] Found code style errors"
                                    " (and warnings).")


if __name__ == "__main__":
    unittest.main()
