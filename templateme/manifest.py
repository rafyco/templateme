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

import os
import json

class ManifestError(Exception):
    pass


class Manifest(object):
    def _read_argument(self, key, default=""):
        if key in self.data:
            return self.data[key]
        else:
            return default
    def __init__(self, data, template):
        self.data = data

        self.short_description = self._read_argument("short-description", "No description")
        self.description = self._read_argument("description", "No description")
        self.include = self._read_argument("include", [])
        if not isinstance(self.include, list):
            self.include = [self.include]

        self.args = {}
        args = self._read_argument("args", {})
        self.add_arguments(args)
    def add_arguments(self, args):
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
        if not os.path.isfile(path):
            raise ManifestError("Manifest not exist")
        with open(path) as data_file:
            data = json.load(data_file)
        return Manifest(data, template)

