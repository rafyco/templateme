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
import abc
import os

class TemplateError(Exception):
    pass

class TMPElement(abc.ABC):
    def __init__(self, path, template, project_name="Project"):
        self._format = ""
        self.path = re.sub(r"/^{}/".format(template.name), project_name, path)
        print(self.path)
        self.template = template
    @abc.abstractclassmethod
    def load_txt(self):
        raise NotImplementedError
    @property
    def text(self):
        if self._format == "":
            self._format = self.template.manager.render_template_txt(self.load_txt(), self.template)
        return self._format
    def save_element(self, path, debug=False):
        if debug:
            print("Saving: ", os.path.join(path, self.path))
            print(self.text)
        else:
            new_path = os.path.join(path, self.path)
            try:
                os.makedirs(os.path.dirname(new_path))
            except FileExistsError:
                pass
            file = open(new_path, "a")
            file.write(self.text)
            file.close()
            print("save file: ", new_path)

class Template(abc.ABC):
    def __init__(self, name, manager):
        self.manager = manager
        self.name = name
        self._id = self.name
    def __str__(self):
        return "{}".format(self.name)
    @abc.abstractclassmethod
    def get_elements(self):
        raise NotImplementedError()
    @property
    def id(self):
        return self._id
    def save_all(self, path, debug=False, project_name="Project"):
        if os.path.isdir(path):
            raise TemplateError("File '{}' exist".format(path))
        for element in self.get_elements():
            element.save_element(path, debug=debug, project_name=project_name)


class TMPSource(abc.ABC):
    def __init__(self, manager):
        self.manager = manager
    @abc.abstractclassmethod
    def get_all_templates(self):
        raise NotImplementedError()
    def get_template(self, id):
        for template in self.get_all_templates():
            if template.id == id:
                return template
        return None

