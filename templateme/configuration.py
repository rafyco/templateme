#!/usr/bin/env python3
"""
Configuration files for TemplateMe!

The module contains class which allows configuration terminal console
and all default option in TemplateMe.
"""


class Configuration:
    """ Configuration class. """

    def __init__(self):
        self.__config_files = ['~/.config/templateme.json']

        self.__data = None

        self.__values = {
            "email": "Anonymous@unknown.com",
            "author": "Anonymous"
        }

    def get_val(self, key, default=None):
        """ Get value of option. """
        return self.__values if key in self.__values else default
