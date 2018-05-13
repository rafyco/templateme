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
from templateme.path import PathSource
import datetime

class TMPManagerError(Exception):
    pass

class TMPManager(object):
    def __init__(self, name="Project"):
        self.plugins = []
        self.plugins.append(PathSource(manager=self))
        
        self.email = "annonymous@admin.org"
        self.author = "Annonymous"
        self.name = name
    def get_all_templates(self):
        result = []
        for plug in self.plugins:
            for temp in plug.get_all_templates():
                result.append(temp)
        return result
    def get_template(self, name):
        template = None
        for plug in self.plugins:
            template = plug.get_template(name)
            if template is not None:
                break
        return template
    def render_template_txt(self, txt, template):
        result = txt
        changes = {
            'EMAIL': self.email,
            'AUTHOR': self.author,
            'YEAR': datetime.datetime.now().strftime("%Y"),
            'NAME': self.name
            }
        for key in changes:
            result = result.replace("%{}%".format(key), changes[key])
        return result

