#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import templateme

project = 'templateme'
doc_title = "Templateme Documentation!"
doc_author = "Rafal Kobel"
copyright = '2019, {}'.format(doc_author)

version = templateme.get_version()
release = templateme.get_version()

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.githubpages'
]

templates_path = ['_templates']

source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = []

pygments_style = None
html_theme = 'classic'
html_static_path = ['_static']
htmlhelp_basename = "templatemedoc"

latex_documents = [
    (master_doc, 'templateme.tex', doc_title,
     [doc_author] , "manual")
]

man_page = [
    (master_doc, "templateme", doc_title,
     [doc_author], 1)
]

texinfo_documents = [
    (master_doc, 'templateme', doc_title,
     doc_author, 'templateme', 'Templates for all my projects.',
     'Miscellaneous'),
]

epub_title = doc_title
epub_exclude_files = ['search.html']
