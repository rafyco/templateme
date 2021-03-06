#!/usr/bin/env python3
"""
Module for template from path.
"""
import os
import logging
import templateme
from templateme.manifest import Manifest
from templateme.manifest import ManifestError
import templateme.containers.abstract


class TemplateError(Exception):
    """ Problem with template. """


class PathElement(templateme.containers.abstract.TMPElement):
    """ Class with template's element file from path. """

    def __init__(self, path, localization, template):
        templateme.containers.abstract.TMPElement.__init__(self, path, template)
        self.localization = localization
        self._load_txt = ""

    def load_txt(self):
        """ Load information from file. """
        if self._load_txt == "":
            with open(self.localization) as file_ob:
                self._load_txt = file_ob.read()
        return self._load_txt


class PathTemplate(templateme.containers.abstract.Template):
    """ Class with template from path. """

    def __init__(self, path, name, manager):
        manifest = None
        try:
            manifest = Manifest.create_from_file(os.path.join(path, name, "manifest.json"), self)
        except ManifestError:
            pass
        except PermissionError as ex:
            logging.warning("Cannot read manifest file from %s,\n"
                            "Please try change permissions", path)
            raise TemplateError("Permission error", ex)
        templateme.containers.abstract.Template.__init__(self, name, manager, manifest)
        self._path = os.path.join(path, name)

    def _get_elements(self):
        elements = []
        for root, _, files in os.walk(self._path):
            for name in files:
                full_path = os.path.join(root, name)
                if self._is_ignored(full_path):
                    continue
                path_element = os.path.relpath(full_path, self._path)
                element = PathElement(path_element, full_path, self)
                elements.append(element)
        return elements


class PathSource(templateme.containers.abstract.TMPSource):
    """ Class with path source from directory. """

    def __init__(self, manager, path):
        templateme.containers.abstract.TMPSource.__init__(self, manager)
        self._path = path

    def get_all_templates(self):
        """ Return all templates from directory. """
        logging.debug("Path source, get_templates [%s]", self._path)
        templates = []
        logging.debug(self._path)
        templates_path = os.listdir(self._path)
        for temp_file in templates_path:
            if not os.path.isdir(os.path.join(self._path, temp_file)):
                continue
            try:
                templates.append(PathTemplate(self._path, temp_file, self.manager))
            except TemplateError:
                logging.warning("Problem with template crated [%s]"
                                "", os.path.join(self._path, temp_file))
        return templates
