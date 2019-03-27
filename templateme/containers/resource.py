#!/usr/bin/env python3
"""
Module for template from resource.
"""
from os.path import join
import logging
import pkg_resources
import templateme
from templateme.manifest import Manifest
from templateme.manifest import ManifestError
import templateme.containers.abstract


class ResourceElement(templateme.containers.abstract.TMPElement):
    """ Class with template's element file from path. """

    def __init__(self, path, template, localization, name):
        templateme.containers.abstract.TMPElement.__init__(self, path, template)
        self.localization = localization
        self.__load_txt = None
        self.name = name

    def load_txt(self):
        """ Load information from file. """
        if self.__load_txt is None:
            full_path = join(self.localization, self.name, self.path)
            self.__load_txt = pkg_resources.resource_string("templateme", full_path).decode("utf-8")
        return self.__load_txt


class ResourceTemplate(templateme.containers.abstract.Template):
    """ Class with template from path. """

    def __init__(self, name, manager, package_localization="templates"):
        manifest = None
        try:
            manifest_path = join(package_localization, name, "manifest.json")
            json_str = pkg_resources.resource_string("templateme", manifest_path)
            manifest = Manifest.create_from_string(json_str.decode("utf-8"), self)
        except ManifestError:
            pass
        templateme.containers.abstract.Template.__init__(self, name, manager, manifest)
        self.__package_localization = package_localization

    def __search_in_dir(self, package_localization, name, path_in, elements):
        """ Search in directory. """
        where_look = join(package_localization, name)
        where_look = join(where_look, path_in)
        for directory_name in pkg_resources.resource_listdir("templateme", where_look):
            directory_path = join(where_look, directory_name)
            if self._is_ignored(directory_path):
                continue
            if pkg_resources.resource_isdir("templateme", directory_path):
                self.__search_in_dir(package_localization,
                                     name,
                                     join(path_in, directory_name),
                                     elements)
            else:
                resource_element = ResourceElement(join(path_in, directory_name),
                                                   self,
                                                   package_localization,
                                                   name)
                elements.append(resource_element)

    def _get_elements(self):
        elements = []
        self.__search_in_dir(self.__package_localization, self.name, "", elements)
        return elements


class ResourceSource(templateme.containers.abstract.TMPSource):
    """ Class with path source from directory. """

    def __init__(self, manager, source_dir="templates"):
        templateme.containers.abstract.TMPSource.__init__(self, manager)
        self.__templates_elem = source_dir

    def get_all_templates(self):
        """ Return all templates from directory. """
        templates = []
        logging.debug(self.__templates_elem)
        for temp_name in pkg_resources.resource_listdir("templateme", self.__templates_elem):
            templates.append(ResourceTemplate(temp_name, self.manager, self.__templates_elem))
        return templates
