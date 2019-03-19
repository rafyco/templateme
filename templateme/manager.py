#!/usr/bin/env python3
"""
Module of template's manager.
"""
import datetime
from templateme.containers.path import PathSource


class TMPManagerError(Exception):
    """ Manager error. """


class TMPManager:
    """ Template manager. """

    def __init__(self, name="Project"):
        self.plugins = []
        self.plugins.append(PathSource(manager=self))

        self.email = "annonymous@admin.org"
        self.author = "Annonymous"
        self.name = name

    def get_all_templates(self):
        """ Return all of available templates from all of containers. """
        result = []
        for plug in self.plugins:
            for temp in plug.get_all_templates():
                result.append(temp)
        return result

    def get_template(self, name):
        """ Return template by name. """
        template = None
        for plug in self.plugins:
            template = plug.get_template(name)
            if template is not None:
                break
        return template

    def render_template_txt(self, txt, template):
        """ Rendering template to text format. """
        result = txt
        changes = {
            'EMAIL': self.email,
            'AUTHOR': self.author,
            'YEAR': datetime.datetime.now().strftime("%Y"),
            'NAME': self.name
        }
        changes.update(template.args)
        for key in changes:
            result = result.replace("%{}%".format(key.upper()), changes[key])
        return result
