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
Create new project in defined place..

Example usage
=============

To invoke program type in your console::

    templateme -t <template_name> -p <your_project_name>

or::

    python3 -m templateme -t <template_name> -p <your_project_name>

for more option call program with flag C{--help}
"""

from __future__ import unicode_literals
from __future__ import print_function
import logging
import os
from argparse import ArgumentParser
from templateme import get_version
from templateme.manager import TMPManager
from templateme.abstract import Template
from templateme.abstract import TemplateError


def __option_args(argv=None):
    """
    Parsing argument for command line program.

    @param argv: Option parameters
    @type argv: list
    @return: parsed arguments
    """
    parser = ArgumentParser(description="Create new project from template",
                            prog='templateme')
    parser.add_argument("-v", "--version", action='version',
                        version='%(prog)s {}'.format(get_version()))
    parser.add_argument("-d", "--log", dest="logLevel",
                        choices=['DEBUG', 'INFO', 'WARNING',
                                 'ERROR', 'CRITICAL'],
                        help="Set the logging level")
    parser.add_argument("-p", "--project-name", metavar="NAME",
                        dest="project_name", default="project",
                        help="Project name")
    parser.add_argument("-l", "--list", action="store_true",
                        dest="list", default=False,
                        help="List available templates")
    parser.add_argument("-s", "--short-list", action="store_true",
                        dest="short_list", default=False,
                        help="Templates list wihtout description")
    parser.add_argument("-q", "--quite", action="store_true",
                        dest="quite", default=False,
                        help="Not ask about arguments")
    parser.add_argument("-t", "--temp", metavar="TEMPLATE",
                        dest="template", default="",
                        help="Template name")
    return parser.parse_args(argv)


def set_template_arguments(template):
    for key, value in template.args.items():
        default_str = ""
        if value is not None and value != "":
            default_str = " (default: {})".format(value)
        input_str = input("Write ['{}'] value{}: ".format(key, default_str))
        if input_str is "":
            input_str = value
        template.set_argument(key, input_str)
        

def main(argv=None):
    """
    Main function for command line program.

    @param argv: Option parameters
    @type argv: list
    """
    options = __option_args(argv)
    logging.basicConfig(format='%(asctime)s - %(name)s - '
                               '%(levelname)s - %(message)s',
                        level=options.logLevel)
    manager = TMPManager(options.project_name)
    if options.list or options.short_list:
        templates = manager.get_all_templates()
        for temp in templates:
            if options.short_list:
                print("{} ".format(temp))
            else:
                print("* {} - {}".format(temp, temp.short_description))
        exit(0)
    elif options.template == "":
        print("You should define template's name\nSee --help for more information")
        exit(1)

    template = manager.get_template(options.template)
    assert(isinstance(template, Template))
    if template is None:
        print("There are not template name: ", options.template)
        exit(1)
    if not options.quite:
        set_template_arguments(template)
    try:
        template.save(options.project_name, options.project_name)
    except TemplateError as ex:
        print("Cannot save: ", ex)
        exit(2)


if __name__ == "__main__":
    main()
