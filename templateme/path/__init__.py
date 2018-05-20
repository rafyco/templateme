#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###########################################################################
#                                                                         #
#  Copyright (C) 2018  Rafal Kobel <rafalkobel@rafyco.pl>                 #
#                                                                         #
#  This program is free software: you can redistribute it and/or modify   #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation, either version 3 of the License, or      #
#  (at your option) any later version.                                    #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the           #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                         #
###########################################################################
"""

"""
from templateme.manifest import Manifest
from templateme.manifest import ManifestError
import templateme
import templateme.abstract
import logging
import os

class PathElement(templateme.abstract.TMPElement):
    def __init__(self, path, localization, template):
        templateme.abstract.TMPElement.__init__(self, path, template)
        self.localization = localization
        self._load_txt = ""
    def load_txt(self):
        if self._load_txt is "":
            with open(self.localization) as f:
                self._load_txt = f.read()
            f.closed
        return self._load_txt


class PathTemplate(templateme.abstract.Template):
    def __init__(self, path, name, manager):
        manifest = None
        try:
            manifest = Manifest.create_from_file(os.path.join(path, name, "manifest.json"), self)
        except ManifestError:
            pass
        templateme.abstract.Template.__init__(self, name, manager, manifest)
        self._path = os.path.join(path, name)
    def _get_elements(self):
        elements = []
        for root, dirs, files in os.walk(self._path):
            for name in files:
                full_path = os.path.join(root, name)
                if self._is_ignored(full_path):
                    continue
                path_element = os.path.relpath(full_path, self._path)
                element = PathElement(path_element, full_path, self)
                elements.append(element)
        return elements


class PathSource(templateme.abstract.TMPSource):
    def __init__(self, manager, path = os.path.join(templateme.__path__[0], "templates")):
        templateme.abstract.TMPSource.__init__(self, manager)
        self._path = path
    def get_all_templates(self):
        templates = []
        logging.debug(self._path)
        temp = os.listdir(self._path)
        for t in temp:
            templates.append(PathTemplate(self._path, t, self.manager))
        return templates

