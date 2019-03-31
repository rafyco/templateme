#!/usr/bin/env python3
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

import logging
from argparse import ArgumentParser
from templateme import get_version
from templateme.manager import TMPManager
from templateme.containers.abstract import Template
from templateme.containers.abstract import TemplateError


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
                        default='ERROR',
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
    """ Set argument for template. """
    for key, value in template.args.items():
        default_str = ""
        if value is not None and value != "":
            default_str = " (default: {})".format(value)
        input_str = input("Write '{}' value{}: ".format(key, default_str))
        print("{} = {}".format(key, input_str))
        if input_str == "":
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
        print("Heres a list of all templates:\n")
        for temp in templates:
            if options.short_list:
                print("{} ".format(temp))
            else:
                print(" * {} - {}".format(temp, temp.short_description))
        exit(0)
    elif options.template == "":
        print("You should define template's name\nSee --help for more information")
        exit(1)

    template = manager.get_template(options.template)
    assert isinstance(template, Template)
    if template is None:
        print("There are not template name: ", options.template)
        exit(1)
    try:
        if not options.quite:
            template.can_save(options.project_name)
            set_template_arguments(template)
        template.save(options.project_name, options.project_name)
    except TemplateError as ex:
        print("Cannot save: ", ex)
        exit(2)


if __name__ == "__main__":
    main()
