#!/usr/bin/env python3
"""
Testing module templates.
"""

import unittest
from templateme.containers.abstract import TMPSource
from templateme.containers.abstract import Template


class TemplateTested(Template):
    """ Template object for testing. """

    def __init__(self, name, test_key):
        Template.__init__(self, name, None)
        self.test_key = test_key

    @classmethod
    def _get_elements(cls):
        return None


# This is tested class. Can have too many method
class TestTemplatesModule(unittest.TestCase):  # pylint: disable=R0904
    """ Module testsCase. """

    def test_source_template(self):
        """ Test if template source works ok. """
        class SourceTestTemplate(TMPSource):
            """ Tested source Template. """

            def __init__(self):
                TMPSource.__init__(self, None)

            def get_all_templates(self):
                return [TemplateTested("tested_temp", "test")]

        source = SourceTestTemplate()

        self.assertEqual(source.get_template("tested_temp").test_key, "test")
        self.assertIsNone(source.get_template("not_exist"))

if __name__ == "__main__":
    unittest.main()
