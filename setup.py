#!/usr/bin/env python3
"""
Setup file.
"""

from __future__ import unicode_literals
import os
import sys
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
REQUIRED_PYTHON = (3, 6)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of Templateme requires Python {}.{}, but you're trying to
install it on Python {}.{}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have python {}.{} or newer, then try again:
    $ python3 -m pip install --upgrade pip setuptools
    $ pip3 install templateme
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON + REQUIRED_PYTHON)))
    sys.exit(1)

EXCLUDE_FROM_PACKAGES = ['templateme.templates']

version = __import__('templateme').get_version()


def package_data():
    result = []
    for root, dirs, files in os.walk('./templateme/templates'):
        for name in files:
            full_path = os.path.join(root, name)
            result.append(full_path.replace("./templateme/", "./"))
    return {'templateme': result}

tests_req=[
        'pylint==2.3.1',
        'mock==3.0.5',
        'mypy==0.720',
        'pycodestyle==2.5.0'
    ]

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
    test_suite='tests',
    classifiers=[
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Topic :: Terminals'
    ],
    install_requires=[
    ],
    tests_require=tests_req,
    extras_require={
        'documentation': [ 'Sphinx==1.8.4' ],
        'toxtests': tests_req
    },
    entry_points={
        'console_scripts': [
            'templateme = templateme.console:main',
        ]
    },
    command_options={
        'build_sphinx': {
            'project': ('setup.py', "templateme"),
            'version': ('setup.py', version),
            'release': ('setup.py', version),
            'source_dir': ('setup.py', "docs")
        }
    },
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    platforms="Any",
    keywords="template, programming, fast",
    project_urls={
        "Bug Reports": "https://github.com/rafyco/templateme/issues",
        "Source": "https://github.com/rafyco/templateme",
        "Documentation": "https://templateme.readthedocs.io/en/latest/"
    }
)
