#!/usr/bin/env python
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

    templateme [-o url] -t <template_name>

or::

    python3 -m templateme.console [-o url] -t <template_name>

for more option call program with flag C{--help}
"""

from __future__ import unicode_literals
from __future__ import print_function
import logging
from argparse import ArgumentParser
from templateme import get_version


def __option_args(argv=None):
    """
    Parsing argument for command line program.

    @param argv: Option parameters
    @type argv: list
    @return: parsed arguments
    """
    parser = ArgumentParser(description="Save one or more urls from "
                                        "Youtube to file.",
                            prog='ytdown')
    parser.add_argument("-v", "--version", action='version',
                        version='%(prog)s {}'.format(get_version()))
    parser.add_argument("-d", "--log", dest="logLevel",
                        choices=['DEBUG', 'INFO', 'WARNING',
                                 'ERROR', 'CRITICAL'],
                        help="Set the logging level")
    parser.add_argument("-o", "--output", metavar="FILE",
                        dest="output", default="",
                        help="Destination folder.")
    parser.add_argument("-l", "--list", action="store_true",
                        dest="list", default=False,
                        help="List available templates")
    parser.add_argument("-t", "--temp", metavar="TEMPLATE",
                        dest="template", default="")


    return parser.parse_args(argv)

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


if __name__ == "__main__":
    main()
