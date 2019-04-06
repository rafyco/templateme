#!/usr/bin/env python3
"""
Module with abstract classes.
"""
import fnmatch
import abc
import os
import re
from templateme.arguments import empty_args


class TemplateError(Exception):
    """ Class describe template error. """


class TMPElement(abc.ABC):
    """ Class with one of files in template. """
    def __init__(self, path, template, project_name="project"):
        self._format = ""
        self.path = path
        self.template = template
        self.project_name = project_name

    @classmethod
    def load_txt(cls):
        """ Load text. """
        raise NotImplementedError

    @property
    def text(self):
        """ Element text. """
        if self._format == "":
            self._format = self.template.manager.render_template_txt(self.load_txt(), self.template)
        return self._format

    @property
    def save_path(self):
        """ Path to save element in output directory. """
        return self.template.manager.render_template_txt(self.path, self.template)

    def print_element(self):
        """ Print path and source of element. """
        print("{selector}\n{el_path}\n{selector}\n{el_source}\n{selector}\n\n"
              "".format(selector="--------",
                        el_path=self.save_path,
                        el_source=self.text))

    def save(self, path, project_name="project"):
        """ Save element in project. """
        save_path = os.path.join(path, self.save_path)
        save_path = re.sub(r"/^{}/".format(self.template.name), project_name, save_path)
        try:
            os.makedirs(os.path.dirname(save_path))
        except FileExistsError:
            pass
        file = open(save_path, "w")
        file.write(self.text)
        file.close()
        print("save file: ", save_path)


class Template(abc.ABC):
    """ Class which describe template. """
    def __init__(self, name, manager, manifest=None):
        self.manager = manager
        self._name = name

        self._ignored = ['manifest.json', '*.swp', "__pycache__", '*.pyc']
        self._include_templates = None
        self._all_args = None
        self._all_elements = None
        self.__args = None
        self.__args_updated = False
        self._includes = []
        self.manifest = manifest
        if self.manifest:
            for include in self.manifest.include:
                self._includes.append(include)
            self.__args = manifest.args
        else:
            self.__args = empty_args()

    @property
    def args(self):
        """ Arguments with manifest updated file. """
        if not self.__args_updated:
            for inc in self.include_templates:
                self.__args.update(inc.args)
            self.__args_updated = True
        return self.__args

    def add_ignored(self, args):
        """ Add ignore pattern. """
        if isinstance(args, list):
            for elem in args:
                self._ignored.append(elem)
        elif isinstance(args, str):
            self._ignored.append(args)
        else:
            raise AttributeError("Argument should have type 'list' or 'str'")

    def _is_ignored(self, full_path):
        """ Tell if path file is ignored. """
        for ignor in self._ignored:
            if fnmatch.fnmatch(full_path, "*/" + ignor):
                return True
        return False

    def __str__(self):
        return self._name

    @classmethod
    def _get_elements(cls):
        """ Get one of the file's elements. """
        raise NotImplementedError()

    @property
    def name(self):
        """ Name of template. """
        return self._name

    @property
    def include_templates(self):
        """ List of included template. """
        if self._include_templates is None:
            result = []
            for inc in self._includes:
                result.append(self.manager.get_template(inc))
            self._include_templates = result
        return self._include_templates

    @property
    def elements(self):
        """ List of all template's elements. """
        if self._all_elements is None:
            result = self._get_elements()
            for inc in self.include_templates:
                for element in inc.elements:
                    element.template = self
                    result.append(element)
            return result
        return self._all_elements

    @property
    def short_description(self):
        """ Return short description. """
        if self.manifest:
            return self.manifest.short_description
        return "no description"

    @property
    def description(self):
        """ Return long description. """
        if self.manifest:
            return self.manifest.description
        return "no description"

    @classmethod
    def examine_save(cls, path, force=False):
        """ Check if template can be save. """
        if force:
            return
        if os.path.isdir(path):
            raise TemplateError("File '{}' already exist".format(path))

    def print_elements(self):
        """ Print elements on the screen. """
        for element in self.elements:
            element.print_element()

    def save(self, path, project_name=None, force=False):
        """ Save template in path. """
        if self.args.missing_args:
            raise TemplateError("Args {} not Set".format(self.args.missing_args))
        if project_name == "":
            project_name = self.name
        elif project_name is None:
            self.print_elements()
            return
        self.examine_save(path, force=force)
        for element in self.elements:
            element.save(path, project_name=project_name)


class TMPSource(abc.ABC):
    """ Class manage one of the containers. """

    def __init__(self, manager):
        self.manager = manager
        self._templates = None

    @classmethod
    def get_all_templates(cls):
        """ Get list of all templates. """
        raise NotImplementedError()

    @property
    def templates(self):
        """ List of all templates. """
        if self._templates is None:
            self._templates = self.get_all_templates()
        return self._templates

    def get_template(self, name):
        """ Get one of templates by id. """
        for template in self.templates:
            if template.name == name:
                assert isinstance(template, Template)
                return template
        return None
