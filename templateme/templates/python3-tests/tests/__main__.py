#!/usr/bin/env python3
"""
CommandLine interface for test.

For checking tests call::

    python -m %MODULE%.tests
"""

# pylint: disable=W0611
from __future__ import unicode_literals
import unittest
from %MODULE%.tests import Test%MODULE%Module


if __name__ == "__main__":
    unittest.main()
