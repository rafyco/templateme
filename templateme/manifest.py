#!/usr/bin/env python3
"""
Module to parsing manifest file.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional, TYPE_CHECKING

from templateme.arguments import ArgumentsContainer

if TYPE_CHECKING:
    from templateme.containers.abstract import Template  # pylint: disable=R0401


class ManifestError(Exception):
    """ Manifest error. """


class Manifest:
    """ Manifest parsing class. """

    def _read_str_argument(self, key: str, default: str = "") -> str:
        if key in self.data:
            result = self.data[key]
            if isinstance(result, str):
                return result
        return default

    def _read_list_argument(self, key: str, default: Optional[List[str]] = None) -> List[Any]:
        if key in self.data:
            result = self.data[key]
            if isinstance(result, str):
                return [result]
            if isinstance(result, list):
                return result
        return default if isinstance(default, list) else []

    def _read_dict_argument(self,
                            key: str,
                            default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if key in self.data:
            result = self.data[key]
            if isinstance(result, dict):
                return result
        return default if isinstance(default, dict) else {}

    def __init__(
            self,
            data: Dict[str, Any],
            template: 'Template'
    ) -> None:
        self.data = data

        self.short_description = self._read_str_argument("short-description", "No description")
        self.description = self._read_str_argument("description", "No description")
        self.include = self._read_list_argument("include")
        self.template = template

        self.args = ArgumentsContainer.create_from_dict(self._read_list_argument("args", None))

    @staticmethod
    def create_from_file(
            path: str,
            template: 'Template'
    ) -> 'Manifest':
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
    def create_from_string(
            text: str,
            template: 'Template'
    ) -> 'Manifest':
        """ Create manifest object from string. """
        data = json.loads(text)
        return Manifest(data, template)
