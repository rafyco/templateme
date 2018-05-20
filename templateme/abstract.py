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
import fnmatch
import abc
import os
import re

class TemplateError(Exception):
    pass

class TMPElement(abc.ABC):
    def __init__(self, path, template, project_name="project"):
        self._format = ""
        self.path = path
        self.template = template
    @abc.abstractclassmethod
    def load_txt(self):
        raise NotImplementedError
    @property
    def text(self):
        if self._format == "":
            self._format = self.template.manager.render_template_txt(self.load_txt(), self.template)
        return self._format
    def save(self, path, project_name="project"):
        save_path = os.path.join(path, self.path)
        save_path = re.sub(r"/^{}/".format(self.template.name), project_name, save_path)
        save_path = self.template.manager.render_template_txt(save_path, self.template)
        try:
            os.makedirs(os.path.dirname(save_path))
        except FileExistsError:
            pass
        file = open(save_path, "a")
        file.write(self.text)
        file.close()
        print("save file: ", save_path)


class Template(abc.ABC):
    def __init__(self, name, manager, manifest=None):
        self.manager = manager
        self.id = name
        
        self._ignored = ['manifest.json', '*.swp']
        self._include_templates = None
        self._all_args = None
        self._all_elements = None
        self._args = {}
        self._includes = []
        self.manifest = manifest
        if self.manifest:
            for include in self.manifest.include:
                self._includes.append(include)
            self._args = manifest.args
    def add_ignored(self, args):
        if isinstance(args, list):
            for elem in args:
                self._ignored.append(elem)
        elif isinstance(args, str):
            self._isignored.append(args)
        else:
            raise AttributeError("Argument should have type 'list' or 'str'")
    def set_argument(self, key, value):
        self.args[key] = value
    def _is_ignored(self, full_path):
        for ignor in self._ignored:
            if fnmatch.fnmatch(full_path, "*/" + ignor):
                return True
        return False
    def __str__(self):
        return self.id
    @abc.abstractclassmethod
    def _get_elements(self):
        raise NotImplementedError()
    @property
    def name(self):
        return self.id
    @property
    def include_templates(self):
        if self._include_templates is None:
            result = []
            for inc in self._includes:
                result.append(self.manager.get_template(inc))
            self._include_templates = result
        return self._include_templates
    @property
    def args(self):
        if self._all_args is None:
            result = self._args
            for inc in self.include_templates:
                result.update(inc.args)
            self._all_args = result
        return self._all_args

    @property
    def elements(self):
        if self._all_elements is None:
            result = self._get_elements()
            for inc in self.include_templates:
                for element in inc.elements:
                    element.template = self
                    result.append(element)
            return result
        return self._all_elements
                
    @property
    def short_description(self):
        if self.manifest:
            return self.manifest.short_description
        return "no description"

    @property
    def description(self):
        if self.manifest:
            return self.manifest.description
        return "no description"

    @property
    def missing_args(self):
        result = []
        for arg, value in self.args.items():
            if value is None or value == "":
                result.append(arg)
        return result

    def save(self, path, project_name=""):
        if len(self.missing_args) > 0:
            raise TemplateError("Args {} not Set".format(self.missing_args))
        if project_name == "":
            project_name = self.name
        if os.path.isdir(path):
            raise TemplateError("File '{}' already exist".format(path))
        for element in self.elements:
            element.save(path, project_name=project_name)


class TMPSource(abc.ABC):
    def __init__(self, manager):
        self.manager = manager
        self._templates = None
    @abc.abstractclassmethod
    def get_all_templates(self):
        raise NotImplementedError()
    @property
    def templates(self):
        if self._templates is None:
            self._templates = self.get_all_templates()
        return self._templates
    def get_template(self, id):
        for template in self.templates:
            if template.id == id:
                return template
        return None

