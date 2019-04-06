#!/usr/bin/env python3
""" Module to manage template's arguments. """


class ArgumentError(Exception):
    """ Argument error. """


class Argument:
    """ One of argument. """
    def __init__(self,
                 name,
                 required=True,
                 default="",
                 question=None,
                 description=None):
        self.__name = name.lower()
        self.__required = required
        self.default = default if default is not None else ""
        default_question = "Put the '{value}' value"
        self.__question = question if question is not None and question != "" else default_question
        self.description = description if description is not None and description != "" \
            else "Value of '{}'".format(name)
        if self.default != "":
            self.description = "{} (default: {})".format(self.description, self.default)
        self.__value = None

    @staticmethod
    def create_from_dict(dictionary):
        """ Create argument from dictionary element. """
        assert isinstance(dictionary, dict)
        if 'name' not in dictionary:
            raise ArgumentError("Invalid format of argument object")
        name = dictionary['name']
        required = dictionary['required'] if 'required' in dictionary else True
        default = dictionary['default'] if 'default' in dictionary else ""
        question = dictionary['question'] if 'question' in dictionary else None
        description = dictionary['description'] if 'description' in dictionary else None
        return Argument(name, required, default, question, description)

    @property
    def name(self):
        """ Name of argument. """
        return self.__name.upper()

    @property
    def value(self):
        """ Value of argument. """
        if self.__value is None:
            return self.default
        return self.__value

    @value.setter
    def value(self, value):
        """ Set value. """
        self.__value = value

    @property
    def is_set(self):
        """ True if set, False otherwise. """
        if not self.__required:
            return True
        return self.__value is not None

    @property
    def question(self):
        """ String of question about value. """
        return self.__question.format(value=self.name)

    def __str__(self):
        return self.__name


class ArgumentsContainer:
    """ Manager with information about arguments. """
    def __init__(self, args):
        self.__arguments = {}
        if args is None:
            return
        if isinstance(args, list):
            for key in args:
                self.__add_argument(key)
        else:
            raise ArgumentError("Cannot add element type: {}".format(type(args)))

    def __add_argument(self, arg, value=None):
        """ Add one argument. """
        new_element = Argument.create_from_dict(arg)
        if new_element.name in self.__arguments:
            raise ArgumentError("Cannot add element {} twice".format(new_element.name))
        if value is not None:
            new_element.value = value
        self.__arguments[new_element.name.lower()] = new_element

    @property
    def missing_args(self):
        """ Return all argument that is not set. """
        result = []
        for key in self.__arguments:
            if not self.__arguments[key].is_set:
                result.append(self.__arguments[key])
        return result

    @property
    def all(self):
        """ List of all elements. """
        return self.__arguments

    def input_missing(self):
        """ Ask about all missing arguments. """
        for argument in self.missing_args:
            input_str = input("{}: ".format(argument.question))
            argument.value = input_str

    def add_values(self, list_of_values):
        """ Add value of element. """
        assert isinstance(list_of_values, dict)
        for key in list_of_values:
            if key.lower() in self.__arguments:
                self.__arguments[key.lower()].value = list_of_values[key]
            else:
                new_argument = Argument(key)
                new_argument.value = list_of_values[key]
                self.__arguments[key.lower()] = new_argument

    def get_argument(self, key):
        """ Get argument by key. """
        return self.__arguments[key.lower()]

    def update(self, arguments):
        """ Update values of arguments. """
        assert isinstance(arguments, ArgumentsContainer) or arguments is None
        for key in arguments.all:
            if key in self.__arguments:
                this_arg = self.__arguments[key]
                if this_arg.default == "":
                    this_arg.default = arguments.all[key].default
            else:
                self.__arguments[key.lower()] = arguments.all[key]


def empty_args():
    """ Crate ArgumentContainer for empty arguments list. """
    return ArgumentsContainer(None)
