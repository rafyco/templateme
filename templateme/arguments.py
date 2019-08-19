#!/usr/bin/env python3
""" Module to manage template's arguments. """
import logging
from typing import Optional, Dict, Any, List


class ArgumentError(Exception):
    """ Argument error. """


class Argument:
    """ One of argument. """
    def __init__(self,
                 name: str,
                 required: bool = True,
                 default: str = "",
                 question: str = "",
                 description: str = "") -> None:
        self.__name = name.lower()
        self.__required = required
        self.default = default
        default_question = "Put the '{value}' value"
        self.__question = question if question != "" else default_question
        self.description = description if description != "" \
            else "Value of '{}'".format(name)
        if self.default != "":
            self.description = "{} (default: {})".format(self.description, self.default)
        self.__value: Optional[str] = None

    @staticmethod
    def create_from_dict(dictionary: Dict[str, Any]) -> 'Argument':
        """ Create argument from dictionary element. """
        if 'name' not in dictionary:
            raise ArgumentError("Invalid format of argument object")
        name = dictionary['name']
        required = dictionary['required'] if 'required' in dictionary else True
        default = dictionary['default'] if 'default' in dictionary else ""
        question = dictionary['question'] if 'question' in dictionary else ""
        description = dictionary['description'] if 'description' in dictionary else ""
        return Argument(name, required, default, question, description)

    @property
    def name(self) -> str:
        """ Name of argument. """
        return self.__name.upper()

    @property
    def value(self) -> str:
        """ Value of argument. """
        if self.__value is None:
            return self.default
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        """ Set value. """
        self.__value = value

    @property
    def is_set(self) -> bool:
        """ True if set, False otherwise. """
        if not self.__required:
            return True
        return self.__value is not None

    @property
    def question(self) -> str:
        """ String of question about value. """
        return self.__question.format(value=self.name)

    def __str__(self) -> str:
        return self.__name


class ArgumentsContainer:
    """ Manager with information about arguments. """
    def __init__(self, args: Optional[List[Argument]]) -> None:
        self.__arguments: Dict[str, Argument] = {}
        if args is not None:
            for key in args:
                self.__add_argument(key)

    @staticmethod
    def create_from_dict(args: List[Dict[str, Any]]) -> 'ArgumentsContainer':
        """ Create Argument container from dict object. """
        result = []
        for elem in args:
            result.append(Argument.create_from_dict(elem))
        return ArgumentsContainer(result)

    def __add_argument(self, new_element: Argument, value: Optional[str] = None) -> None:
        """ Add one argument. """
        if new_element.name in self.__arguments:
            raise ArgumentError("Cannot add element {} twice".format(new_element.name))
        if value is not None:
            new_element.value = value
        logging.debug("Add argument: %s", new_element.name.lower())
        self.__arguments[new_element.name.lower()] = new_element

    @property
    def missing_args(self) -> List[Argument]:
        """ Return all argument that is not set. """
        result = []
        logging.debug("Missing args: ")
        for key in self.__arguments:
            logging.debug("is missing [%s]", key.lower())
            if not self.__arguments[key].is_set:
                logging.debug("missing [%s]", key.lower())
                result.append(self.__arguments[key])
        return result

    @property
    def all(self) -> Dict[str, Argument]:
        """ List of all elements. """
        return self.__arguments

    def input_missing(self) -> None:
        """ Ask about all missing arguments. """
        for argument in self.missing_args:
            input_str = input("{}: ".format(argument.question))
            argument.value = input_str

    def __update_value(self, key: str, value: str) -> None:
        """ Update value of existing atribute or add new one. """
        if key.lower() in self.__arguments:
            self.__arguments[key.lower()].value = value
        else:
            logging.debug("update value: %s", key.lower())
            new_argument = Argument(key)
            new_argument.value = value
            self.__arguments[key.lower()] = new_argument

    def add_values(self, dict_of_values: Dict[str, str]) -> None:
        """ Add value of element. """
        for key in dict_of_values:
            self.__update_value(key, dict_of_values[key])

    def add_values_from_list(self, list_of_arguments: List[List[str]]) -> None:
        """ Add values from list of 2-elements lists. """
        for argument_elem in list_of_arguments:
            assert isinstance(argument_elem, list) and len(argument_elem) == 2
            self.__update_value(argument_elem[0], argument_elem[1])

    def get_argument(self, key: str) -> Argument:
        """ Get argument by key. """
        return self.__arguments[key.lower()]

    def update(self, arguments: 'ArgumentsContainer') -> None:
        """ Update values of arguments. """
        logging.debug("update")
        for key in arguments.all:
            logging.debug("Add update argument: %s", key.lower())
            if key in self.__arguments:
                this_arg = self.__arguments[key]
                if this_arg.default == "":
                    this_arg.default = arguments.all[key].default
            else:
                self.__arguments[key.lower()] = arguments.all[key]


def empty_args() -> 'ArgumentsContainer':
    """ Crate ArgumentContainer for empty arguments list. """
    return ArgumentsContainer(None)
