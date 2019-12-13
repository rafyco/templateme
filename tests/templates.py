#!/usr/bin/env python3
"""
Testing module templates.
"""

import unittest
from templateme.containers.abstract import TMPSource
from templateme.containers.abstract import Template
from templateme.containers.abstract import TMPElement
from typing import List


class TemplateTested(Template):
    """ Template object for testing. """

    def __init__(self, name, test_key) -> None:
        Template.__init__(self, name, None)
        self.test_key = test_key

    def _get_elements(self) -> List[TMPElement]:
        return []


# This is tested class. Can have too many method
class TestTemplatesModule(unittest.TestCase):  # pylint: disable=R0904
    """ Module testsCase. """

    def test_source_template(self) -> None:
        """ Test if template source works ok. """
        class SourceTestTemplate(TMPSource):
            """ Tested source Template. """

            def __init__(self) -> None:
                TMPSource.__init__(self, None)

            def get_all_templates(self) -> None:
                return [TemplateTested("tested_temp", "test")]

        source = SourceTestTemplate()

        self.assertEqual(source.get_template("tested_temp").test_key, "test")
        self.assertIsNone(source.get_template("not_exist"))


if __name__ == "__main__":
    unittest.main()
