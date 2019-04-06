#!/usr/bin/env python3
"""
Module of template's manager.
"""
import os
import logging
import datetime
from templateme.containers.resource import ResourceSource
from templateme.containers.path import PathSource
from templateme.configuration import Configuration


class TMPManagerError(Exception):
    """ Manager error. """


class TMPManager:
    """ Template manager. """

    def __init__(self, name="Project", debug=False):
        self.plugins = []
        self.__config = Configuration(debug=debug)

        self.__register_sources()
        self.name = name

    def __register_sources(self):
        """ Register all plugins needed by manager. """
        self.plugins.append(ResourceSource(manager=self, source_dir="templates"))
        if self.__config.debug:
            logging.debug("Debug mode, find templates only from package")
            return
        template_path_tab = ["/etc/templateme", "~/.config/templateme"]
        template_path_tab = template_path_tab + self.__config.localizations
        for template_path in template_path_tab:
            template_path = os.path.expanduser(template_path)
            if os.path.isdir(template_path):
                path_source = PathSource(manager=self, path=template_path)
                self.plugins.append(path_source)

    def get_all_templates(self):
        """ Return all of available templates from all of containers. """
        result = []
        for plug in self.plugins:
            logging.debug("get_all_templates [%s]", plug)
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
            'EMAIL': self.__config.get_val('email'),
            'AUTHOR': self.__config.get_val('author'),
            'YEAR': datetime.datetime.now().strftime("%Y"),
            'NAME': self.name if self.name is not None else "console"
        }
        template.args.add_values(changes)
        for key in template.args.all:
            elem = template.args.get_argument(key)
            result = result.replace("%{}%".format(elem.name), elem.value)
        return result
