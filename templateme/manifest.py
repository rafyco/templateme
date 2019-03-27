#!/usr/bin/env python3
"""
Module to parsing manifest file.
"""

import os
import json


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

        self.args = {}
        args = self._read_argument("args", {})
        self._add_arguments(args)

    def _add_arguments(self, args):
        if isinstance(args, list):
            for key in args:
                self.args[key] = None
        elif isinstance(args, dict):
            for key, value in args.items():
                self.args[key] = value
        else:
            raise AttributeError()

    @staticmethod
    def create_from_file(path, template):
        """ Create manifest object from file. """
        if not os.path.isfile(path):
            raise ManifestError("Manifest not exist")
        with open(path) as data_file:
            data = json.load(data_file)
        return Manifest(data, template)

    @staticmethod
    def create_from_string(text, template):
        """ Create manifest object from string. """
        data = json.loads(text)
        return Manifest(data, template)
