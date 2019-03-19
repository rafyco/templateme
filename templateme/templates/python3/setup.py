#!/usr/bin/env python3
import os
import sys
from setuptools import setup


def read_description(module_name):
    module_doc = __import__(module_name).__doc__.splitlines()
    result = ""
    for line in module_doc:
        if line:
            result = line
            break
    return result

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 4)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of %MODULE% requires Python {}.{}, but you're trying to
install it on Python {}.{}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have python 3.4 or newer, then try again:
    $ python3 -m pip install --upgrade pip setuptools
    $ pip3 install %MODULE% 
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

EXCLUDE_FROM_PACKAGES = ['%MODULE%.%MODULE%']

version = __import__('%MODULE%').get_version()


setup(
    name='%MODULE%',
    version=version,
    license='GNU',
    author="%AUTHOR%",
    author_email="%EMAIL%",
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    description=read_description('%MODULE%'),
    long_description=open("README.rst").read(),
    url="%GITHUB%",
    include_package_data=True,
    package_dir={'%MODULE%': '%MODULE%'},
    package_data=package_data(),
    test_suite='%MODULE%.tests.__main__',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'pylint',
        'pep8'
    ],
    keywords=""
)
