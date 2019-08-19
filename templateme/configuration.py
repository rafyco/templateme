#!/usr/bin/env python3
"""
Configuration files for TemplateMe!

The module contains class which allows configuration terminal console
and all default option in TemplateMe.
"""

from configparser import ConfigParser
import os
from typing import List


class Configuration:
    """ Configuration class. """

    default_config = """
[global]
;; Default email name
email=user@unknown.com
;; default user name
author=user
;; default license
license=MIT
;; additional localizations separated by ':' sign
templates=
    """

    def __init__(self, debug: bool = False):
        config_files: List[str] = []
        if not debug:
            config_files = [
                '/etc/templateme/config.ini',
                '~/.config/templateme/config.ini',
                '~/.templateme'
            ]

        default_config = ConfigParser()
        default_config.read_string(Configuration.default_config)
        self.__configurations = [default_config]

        for elem in config_files:
            path_file = os.path.expanduser(elem)
            if not os.path.isfile(path_file):
                continue

            with open(path_file, "r") as config_file:
                new_config = ConfigParser()
                new_config.read_file(config_file)
                self.__configurations.append(new_config)

        self.__debug = debug

    def get_val(self, key: str, section: str = "global", default: str = "") -> str:
        """ Get value of option. """
        for config in reversed(self.__configurations):
            if section in config:
                if key in config[section]:
                    return config[section][key]
        return default

    @property
    def debug(self) -> bool:
        """ Check if configuration is from debug. """
        return self.__debug

    @property
    def localizations(self) -> List[str]:
        """ Localization of all place where application should look for templates. """
        result = []
        locations = self.get_val("templates", default="")
        for location in locations.split(":"):
            path_location = os.path.expanduser(location)
            if os.path.isdir(path_location):
                result.append(path_location)
        return result
