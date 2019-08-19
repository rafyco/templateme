#!/usr/bin/env python3
"""
Module with abstract classes.
"""
import fnmatch
import abc
import logging
import os
import re
from typing import Optional, Any, List, TYPE_CHECKING

from templateme.arguments import empty_args, ArgumentsContainer
from templateme.manifest import Manifest

if TYPE_CHECKING:
    from templateme.manager import TMPManager  # pylint: disable=R0401


class TemplateError(Exception):
    """ Class describe template error. """


class TMPElement(abc.ABC):
    """ Class with one of files in template. """
    def __init__(self, path: str, template: 'Template', project_name: str = "project") -> None:
        self._format: str = ""
        self.path = path
        self.template = template
        self.project_name = project_name

    def load_txt(self) -> str:
        """ Load text. """
        raise NotImplementedError

    @property
    def text(self) -> str:
        """ Element text. """
        if self._format == "":
            self._format = self.template.manager.render_template_txt(self.load_txt(), self.template)
        return self._format

    @property
    def save_path(self) -> str:
        """ Path to save element in output directory. """
        return self.template.manager.render_template_txt(self.path, self.template)

    def print_element(self) -> None:
        """ Print path and source of element. """
        print("{selector}\n{el_path}\n{selector}\n{el_source}\n{selector}\n\n"
              "".format(selector="--------",
                        el_path=self.save_path,
                        el_source=self.text))

    def save(self, path: str, project_name: str = "project") -> None:
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
    def __init__(
            self,
            name: str,
            manager: 'TMPManager',
            manifest: Optional[Manifest] = None
    ) -> None:
        self.manager = manager
        self._name = name

        self._ignored = ['manifest.json', '*.swp', "__pycache__", '*.pyc']
        self._include_templates: Optional[List[Template]] = None
        self._all_args = None
        self._all_elements = None
        self.__args_updated = False
        self._includes: List[str] = []
        self.manifest: Optional[Manifest] = manifest
        if self.manifest is not None:
            for include in self.manifest.include:
                self._includes.append(include)
            self.__args = self.manifest.args
        else:
            self.__args = empty_args()

    @property
    def args(self) -> ArgumentsContainer:
        """ Arguments with manifest updated file. """
        if not self.__args_updated:
            for inc in self.include_templates:
                logging.debug("args %s", inc.args)
                self.__args.update(inc.args)
            self.__args_updated = True
        return self.__args

    def add_ignored(self, args: Any) -> None:
        """ Add ignore pattern. """
        if isinstance(args, list):
            for elem in args:
                self._ignored.append(elem)
        elif isinstance(args, str):
            self._ignored.append(args)
        else:
            raise AttributeError("Argument should have type 'list' or 'str'")

    def _is_ignored(self, full_path: str) -> bool:
        """ Tell if path file is ignored. """
        for ignor in self._ignored:
            if fnmatch.fnmatch(full_path, "*/" + ignor):
                return True
        return False

    def __str__(self) -> str:
        return self._name

    def _get_elements(self) -> List[TMPElement]:
        """ Get one of the file's elements. """
        raise NotImplementedError()

    @property
    def name(self) -> str:
        """ Name of template. """
        return self._name

    @property
    def include_templates(self) -> List['Template']:
        """ List of included template. """
        if self._include_templates is None:
            self._include_templates = []
            for inc in self._includes:
                template = self.manager.get_template(inc)
                if template is not None:
                    self._include_templates.append(template)
        return self._include_templates

    @property
    def elements(self) -> List[TMPElement]:
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
    def short_description(self) -> str:
        """ Return short description. """
        if self.manifest is not None:
            return self.manifest.short_description
        return "no description"

    @property
    def description(self) -> str:
        """ Return long description. """
        if self.manifest is not None:
            return self.manifest.description
        return "no description"

    @classmethod
    def examine_save(cls, path: str, force: bool = False) -> None:
        """ Check if template can be save. """
        if force:
            return
        if os.path.isdir(path):
            raise TemplateError("File '{}' already exist".format(path))

    def print_elements(self) -> None:
        """ Print elements on the screen. """
        for element in self.elements:
            element.print_element()

    def save(self, path: str, project_name: Optional[str] = None, force: bool = False) -> None:
        """ Save template in path. """
        if self.args.missing_args:
            raise TemplateError("cannot set {} arguments. First is [{}]"
                                "".format(len(self.args.missing_args),
                                          self.args.missing_args[0]))
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

    def __init__(
            self,
            manager: 'TMPManager'
    ) -> None:
        self.manager = manager
        self._templates: Optional[List[Template]] = None

    def get_all_templates(self) -> List[Template]:
        """ Get list of all templates. """
        raise NotImplementedError()

    @property
    def templates(self) -> List[Template]:
        """ List of all templates. """
        if self._templates is None:
            self._templates = self.get_all_templates()
        return self._templates

    def get_template(self, name: str) -> Optional[Template]:
        """ Get one of templates by id. """
        for template in self.templates:
            if template.name == name:
                assert isinstance(template, Template)
                return template
        return None
