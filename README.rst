==================================
TemplateMe - Manager for templates
==================================

Console programs to make new project in defined languages.

.. image:: https://img.shields.io/badge/author-Rafa%C5%82%20Kobel-blue.svg
    :target: https://rafyco.pl

.. image:: https://img.shields.io/travis/rafyco/templateme.svg?logo=travis
   :target: https://travis-ci.org/rafyco/templateme

.. image:: https://img.shields.io/github/last-commit/rafyco/templateme.svg?logo=github
    :target: https://github.com/rafyco/templateme

.. image:: https://img.shields.io/readthedocs/templateme.svg
   :target: https://templateme.readthedocs.io

.. image:: https://img.shields.io/pypi/v/templateme.svg?logo=python
   :target: https://pypi.python.org/pypi/templateme/

.. image:: https://img.shields.io/github/license/rafyco/templateme.svg
   :target: https://opensource.org/licenses/mit-license.php


Instalation
-----------

There are two different methods to install ``TemplateMe``. You can install
it from PyPi repository or download sources from github and try to install
it. Please choose one of the methods and install it on you computer.

from PyPi repository
~~~~~~~~~~~~~~~~~~~~

To install TemplateMe from repository you can use pip program.

::

    sudo pip3 install templateme

from sources
~~~~~~~~~~~~

Another option is to install program from github sources. To do this just
get all necessary files using git or by github's zip file and call following
command:

::

    sudo python3 setup.py install

Usage
-----

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

For more information about application please visit the documentation or try:

::

    templateme --help


Author
------

Rafal Kobel <rafalkobel@rafyco.pl>


.. image:: https://img.shields.io/static/v1.svg?label=Linkedin&message=Rafal%20Kobel&color=blue&logo=linkedin
   :target: https://www.linkedin.com/in/rafa%C5%82-kobel-03850910a/

.. image:: https://img.shields.io/static/v1.svg?label=Github&message=rafyco&color=blue&logo=github
   :target: https://github.com/rafyco

.. image:: https://img.shields.io/static/v1.svg?label=Facebook&message=Rafal%20Kobel&color=blue&logo=facebook
    :target: https://facebook.com/rafyco

