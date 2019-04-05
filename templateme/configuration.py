#!/usr/bin/env python3
"""
Configuration files for TemplateMe!

The module contains class which allows configuration terminal console
and all default option in TemplateMe.
"""


class Configuration:
    """ Configuration class. """

    def __init__(self, debug=False):
        self.__config_files = ['~/.config/templateme.json']

        self.__data = None
        self.__debug = debug

        self.__defaults = {
            "EMAIL": "Anonymous@unknown.com",
            "AUTHOR": "Anonymous"
        }

    def get_val(self, key, default=None):
        """ Get value of option. """
        key = key.upper()
        return self.__defaults[key] if key in self.__defaults else default

    @property
    def debug(self):
        """ Check if configuration is from debug. """
        return self.__debug
