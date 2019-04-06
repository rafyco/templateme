#!/usr/bin/env python3
"""
CommandLine interface for test.

For checking tests call::

    python -m templateme.tests
"""

# pylint: disable=W0611
import unittest
from templateme.tests import TestTemplateMeModule
from templateme.tests.console import TestConsoleModule
from templateme.tests.templates import TestTemplatesModule
from templateme.tests.arguments import TestArgumentsModule


if __name__ == "__main__":
    unittest.main()
