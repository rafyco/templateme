#!/usr/bin/env python3
"""
Module to parsing manifest file.
"""

import os
import json
import logging
from templateme.arguments import ArgumentsContainer


class ManifestError(Exception):
    """ Manifest error. """


class Manifest:
    """ Manifest parsing class. """

    def _read_argument(self, key, default=""):
        if key in self.data:
            return self.data[key]
        return default

    def __init__(self, data, template):
        self.data = data

        self.short_description = self._read_argument("short-description", "No description")
        self.description = self._read_argument("description", "No description")
        self.include = self._read_argument("include", [])
        self.template = template
        if not isinstance(self.include, list):
            self.include = [self.include]

        self.args = ArgumentsContainer(self._read_argument("args", []))

    @staticmethod
    def create_from_file(path, template):
        """ Create manifest object from file. """
        if not os.path.isfile(path):
            raise ManifestError("Manifest not exist")
        try:
            with open(path) as data_file:
                data = json.load(data_file)
        except json.decoder.JSONDecodeError:
            logging.warning("Cannot read manifest file [%s]", data_file)
            raise ManifestError("Invalid manifest file")
        return Manifest(data, template)

    @staticmethod
    def create_from_string(text, template):
        """ Create manifest object from string. """
        data = json.loads(text)
        return Manifest(data, template)
