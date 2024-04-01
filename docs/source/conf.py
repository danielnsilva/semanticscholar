# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import datetime
import importlib
import os
import pkgutil
import sys

import pypandoc

# sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.path.join(os.getcwd(), '../..'))

from semanticscholar.SemanticScholarObject import SemanticScholarObject
import re

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'semanticscholar'
copyright = f'{datetime.date.today().year}, Daniel Silva'
author = 'Daniel Silva'

# Get release version from setup.py
with open('../../setup.py', 'r') as setup_file:
    setup_contents = setup_file.read()
release = re.search(r"version=['\"]([^'\"]+)['\"]", setup_contents).group(1)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'm2r2',
    'sphinx_copybutton'
]

templates_path = ['_templates', '../build/html']
html_additional_pages = {'index': 'overview.html'}
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = 'furo'
html_static_path = ['_static']
html_title = 'semanticscholar'

# Both the class’ and the __init__ method’s docstring are concatenated and inserted.
autoclass_content = 'both'

# --- API Endpoints ---

api_endpoints = dict()
className = 'SemanticScholar'
fullClassName = f'semanticscholar.{className}.{className}'
api_file = open(f'../../semanticscholar/{className}.py', encoding="utf8")
for line in api_file:
    line = line.strip()
    while line.endswith('\\'):
        line = line[:-1]
        line += next(api_file).strip()
    if line.startswith('def'):
        method_name = line.split(' ')[1].split('(')[0]
        method = f'{fullClassName}.{method_name}()'
    if line.startswith(':calls:'):
        _, http_method, endpoint, _ = line.split(' ')
        http_method = http_method[1:]
        if endpoint not in api_endpoints:
            api_endpoints[endpoint] = dict()
        if http_method not in api_endpoints[endpoint]:
            api_endpoints[endpoint][http_method] = f':meth:`{method}`'

api_file_contents = 'API Endpoints\n'
api_file_contents += '-------------\n'
for endpoint, methods in sorted(api_endpoints.items()):
    prefix = '/'.join(endpoint.split('/')[:3])
    if prefix not in api_file_contents:
        api_file_contents += f'\n{prefix}\n'
        api_file_contents += f'{"^" * len(prefix)}\n\n'
    endpoint = endpoint[len(prefix):]
    api_file_contents += f'* {endpoint}\n'
    for http_method, method in sorted(methods.items()):
        api_file_contents += f'\t* {http_method}: {method}\n'

api_file = open('api.rst', 'w', encoding='utf-8')
api_file.seek(0)
api_file.write(api_file_contents)
api_file.close()

# --- SemanticScholar objects ---

def find_subclasses(module, base_class):
    '''Return all subclasses of a base class within a module.'''
    subclasses = []
    for _, obj in vars(module).items():
        if (isinstance(obj, type) and
                issubclass(obj, base_class) and
                obj != base_class):
            subclasses.append(obj)
    return subclasses

semantic_scholar_dir = os.path.join(os.getcwd(), '../..', 'semanticscholar')

# Load all modules from the `semanticscholar` directory
modules = []
for (_, module_name, _) in pkgutil.iter_modules([semantic_scholar_dir]):
    module = importlib.import_module(f'semanticscholar.{module_name}')
    modules.append(module)

# Find subclasses
all_subclasses = []
for module in modules:
    all_subclasses.extend(find_subclasses(module, SemanticScholarObject))

# Filter only the subclasses that don't have other subclasses
# and ensure uniqueness using a set
final_subclasses_set = set()
for cls in all_subclasses:
    is_final_subclass = True  # Assume it's a final subclass initially
    for sub in all_subclasses:
        if issubclass(sub, cls) and sub != cls:
            is_final_subclass = False  # It's not a final subclass
            break
    if is_final_subclass:
        final_subclasses_set.add(cls)

# Write main rst file
with open('s2objects.rst', 'w', encoding='utf-8') as s2objects_file:
    s2objects_file.write('SemanticScholar Objects\n')
    s2objects_file.write('-----------------------\n\n')
    s2objects_file.write('.. autoclass:: ' +
        'semanticscholar.SemanticScholarObject.SemanticScholarObject\n')
    s2objects_file.write('\t:members:\n\n')
    s2objects_file.write('.. toctree::\n')
    s2objects_file.write('\t:maxdepth: 1\n\n')
    for cls in sorted(final_subclasses_set, key=lambda x: x.__name__):
        s2objects_file.write(f'\ts2objects/{cls.__name__}\n')

# Write the rst files for each subclass
for cls in sorted(final_subclasses_set, key=lambda x: x.__name__):
    with open(f's2objects/{cls.__name__}.rst', 'w', encoding='utf-8') \
            as s2object_file:
        fullClassName = f'{cls.__module__}.{cls.__name__}'
        s2object_file.write(f'{cls.__name__}\n')
        s2object_file.write(f'{"-" * len(cls.__name__)}\n\n')
        s2object_file.write(f'.. autoclass:: {fullClassName}\n')
        s2object_file.write('\t:members:\n')

# --- Changelog ---

with open('../../CHANGELOG.md', 'r', encoding='utf-8') as changelog_file:
    changelog = changelog_file.read()
    changes_rst = pypandoc.convert_text(changelog, 'rst', format='md')
    changes_rst = ':tocdepth: 2\n\n' + changes_rst
    with open('changes.rst', 'w', encoding='utf-8') as changes_file:
        changes_file.write(changes_rst)
