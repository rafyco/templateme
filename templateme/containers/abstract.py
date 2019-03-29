#!/usr/bin/env python3
"""
Module with abstract classes.
"""
import fnmatch
import abc
import os
import re


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

    def save(self, path, project_name="project"):
        """ Save element in project file. """
        save_path = os.path.join(path, self.path)
        save_path = re.sub(r"/^{}/".format(self.template.name), project_name, save_path)
        save_path = self.template.manager.render_template_txt(save_path, self.template)
        try:
            os.makedirs(os.path.dirname(save_path))
        except FileExistsError:
            pass
        file = open(save_path, "a")
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
        self._args = {}
        self._includes = []
        self.manifest = manifest
        if self.manifest:
            for include in self.manifest.include:
                self._includes.append(include)
            self._args = manifest.args

    def add_ignored(self, args):
        """ Add ignore pattern. """
        if isinstance(args, list):
            for elem in args:
                self._ignored.append(elem)
        elif isinstance(args, str):
            self._ignored.append(args)
        else:
            raise AttributeError("Argument should have type 'list' or 'str'")

    def set_argument(self, key, value):
        """ Set one of arguments. """
        self.args[key] = value

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
    def args(self):
        """ List of all arguments. """
        if self._all_args is None:
            result = self._args
            for inc in self.include_templates:
                result.update(inc.args)
            self._all_args = result
        return self._all_args

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

    @property
    def missing_args(self):
        """ List of missing arguments. """
        result = []
        for arg, value in self.args.items():
            if value is None or value == "":
                result.append(arg)
        return result

    @classmethod
    def can_save(cls, path):
        """ Check if template can be save. """
        if os.path.isdir(path):
            raise TemplateError("File '{}' already exist".format(path))

    def save(self, path, project_name=""):
        """ Save template in path. """
        if self.missing_args:
            raise TemplateError("Args {} not Set".format(self.missing_args))
        if project_name == "":
            project_name = self.name
        self.can_save(path)
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
                return template
        return None
