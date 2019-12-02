#!/usr/bin/env python3
"""
Create new project in defined place..

The TemplateMe works as console application. It allows you to create new
project from predefined templates. To see list of all available elements
call:

::

    templateme --list

In case that you want to prepare new project for your favourite language
you need to choose one of the templates and write in your terminal:

::

    templateme -t <template_name> -o <your_project_name>

Where ``<template_name>`` is the one of the templates, listed in previous step
and ``<your_project_name>`` is a name of folder with your created project. After
that, the program will ask you to write a few variables that are necessary to
build templates.

"""

import logging
import sys
from argparse import ArgumentParser
from argparse import ArgumentTypeError
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
    def check_arguments(value):
        """ Check if argument value looks ok. """
        valuelist = value.split("=")
        if len(valuelist) != 2:
            raise ArgumentTypeError("Value should have format: argument=value")
        if valuelist[0].strip() == "" or valuelist[1].strip() == "":
            raise ArgumentTypeError("Value and argument name should not be empty")
        return valuelist

    parser = ArgumentParser(description="Create new project from template",
                            prog='templateme')
    parser.add_argument("-v", "--version", action='version',
                        version='%(prog)s {}'.format(get_version()))
    parser.add_argument("-d", "--log", dest="logLevel",
                        choices=['DEBUG', 'INFO', 'WARNING',
                                 'ERROR', 'CRITICAL'],
                        default='ERROR',
                        help="Set the logging level")
    parser.add_argument("-o", "--out", metavar="NAME",
                        dest="project_name", default=None,
                        help="Name of your new project directory")
    parser.add_argument("-l", "--list", action="store_true",
                        dest="list", default=False,
                        help="List available templates")
    parser.add_argument("-s", "--short-list", action="store_true",
                        dest="short_list", default=False,
                        help="Templates list wihtout description")
    parser.add_argument("-a", "--argument", action="append",
                        dest="argvalues", type=check_arguments,
                        default=[],
                        help="List of predefinied arguments")
    parser.add_argument("-q", "--quite", action="store_true",
                        dest="quite", default=False,
                        help="Not ask about arguments")
    parser.add_argument("-t", "--template", metavar="TEMPLATE",
                        dest="template", default="",
                        help="Template name")
    parser.add_argument("-f", "--force", action="store_true",
                        dest="force", default=False,
                        help="Force save template")
    return parser.parse_args(argv)


def print_template(template):
    """ Print information about template. """
    separator = "-----------------------"
    print("{sep}\nTemplate - {name}\n{sep}".format(sep=separator, name=template.name))
    print("{short_desc}\n\n{desc}\n{sep}"
          "".format(sep=separator,
                    short_desc=template.short_description,
                    desc=template.description))
    print("")
    for attribute in template.args.all.values():
        print(" - {} - {}".format(attribute.name, attribute.description))

    print("\n{}\n".format(separator))
    for elem in template.elements:
        print(" * ./{}".format(elem.path))
    print("\n{}".format(separator))


def examine_save(template, project_name, force):
    """
    Check if template exists and you can save it.
    If not, ask about confirmation to do this.
    """
    if force or project_name is None:
        return
    try:
        template.examine_save(project_name)
    except TemplateError:
        # Examine not pass, ask user of it
        input_str = input("File exists. Do you want override the template (y[es]|n[o]): ")
        if input_str in ("yes", "y", "ok"):
            print("Template will be overrided")
        elif input_str in ("no", "n"):
            print("We not override template")
            if input_str not in ("no", "n"):
                print("Next time use one of this answers: y[es]|n[o]")
            raise


def main(argv=None, debug=False):
    """
    Main function for command line program.

    @param argv: Option parameters
    @type argv: list
    """
    options = __option_args(argv)
    logging.basicConfig(format='%(asctime)s - %(name)s - '
                               '%(levelname)s - %(message)s',
                        level=options.logLevel)
    manager = TMPManager(options.project_name, debug=debug)

    if options.list or options.short_list:
        if options.template == "":
            templates = manager.get_all_templates()
            print("Here's a list of all templates:\n")
            for temp in templates:
                if options.short_list:
                    print("{} ".format(temp))
                else:
                    print(" * {} - {}".format(temp, temp.short_description))
            sys.exit(0)
        else:
            template = manager.get_template(options.template)
            print_template(template)
            sys.exit(0)
    elif options.template == "":
        print("You should define template's name\nSee --help for more information")
        sys.exit(1)

    template = manager.get_template(options.template)
    assert isinstance(template, Template)
    if template is None:
        print("There are not template name: ", options.template)
        sys.exit(1)
    force = options.force
    template.args.add_values_from_list(options.argvalues)
    try:
        if not options.quite:
            examine_save(template, options.project_name, force)

            # if examine was confirmed that you want to save template,
            # you can rewrite it even on existing files.
            force = True

            template.args.input_missing()
        template.save(options.project_name, options.project_name, force=force)
    except TemplateError as ex:
        print("Cannot save: ", ex)
        sys.exit(2)


if __name__ == "__main__":
    main()
