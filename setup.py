#!/usr/bin/env python3
from __future__ import unicode_literals
import os
import sys
import codecs
from setuptools import setup
from setuptools import find_packages


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
This version of Templateme requires Python {}.{}, but you're trying to
install it on Python {}.{}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have python 3.4 or newer, then try again:
    $ python3 -m pip install --upgrade pip setuptools
    $ pip3 install templateme
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)
    
EXCLUDE_FROM_PACKAGES = ['templateme.templates']

version = __import__('templateme').get_version()

def package_data():
    result = []
    for root, dirs, files in os.walk('./templateme/templates'):
            for name in files:
                full_path = os.path.join(root, name)
                result.append(full_path.replace("./templateme/", "./"))
    print(result)
    return { 'templateme' : result }

setup(
    name='templateme',
    version=version,
    license='GNU',
    author="Rafal Kobel",
    author_email="rafalkobel@rafyco.pl",
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    description=read_description('templateme'),
    long_description=open("README.rst").read(),
    url="https://github.com/rafyco/templateme",
    include_package_data=True,
    package_dir={'templateme': 'templateme'},
    package_data=package_data(),
    test_suite='templateme.tests.__main__',
    classifiers=[
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    install_requires=[
        'pylint',
        'pep8'
    ],
    entry_points={
        'console_scripts': [
            'templateme = templateme.console:main',
        ]
    },
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    platforms="Any",
    keywords="template, programming, fast"
)
