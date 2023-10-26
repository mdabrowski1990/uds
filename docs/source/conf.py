# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath("."))

import os
import sys
import datetime
import re
try:  # python 3.11 or newer
    import tomlib
except ModuleNotFoundError:
    import tomli as tomlib
sys.path.append(os.path.abspath('../..'))


with open("../../uds/__init__.py", "r", encoding="utf-8") as init_file:
    full_version_from_init = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', init_file.read(), re.MULTILINE).group(1)
    init_file.seek(0)
    author_from_init = re.search(r'^__author__\s*=\s*[\'"]([^\'"]*)[\'"]', init_file.read(), re.MULTILINE).group(1)

with open("../../pyproject.toml", "rb") as pyproject_file:
    _pyproject_data = tomlib.load(pyproject_file)
    project_name_from_pyproject = _pyproject_data["project"]["name"]


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = project_name_from_pyproject
author = author_from_init
copyright = f"{datetime.date.today().year}, {author_from_init}"
version = ".".join(full_version_from_init.split(".")[:2])
release = full_version_from_init


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc",
              "autoapi.extension",
              "sphinx.ext.viewcode",
              "sphinx.ext.graphviz"]

autodoc_typehints = "description"
autodoc_typehints_description_target = "all"


autoapi_type = "python"
autoapi_dirs = ["../../uds"]
autoapi_add_toctree_entry = True
autoapi_generate_api_docs = True
autoapi_options = ["members", "private-members", "special-members", "undoc-members",
                   "show-inheritance", "show-inheritance-diagram", "show-module-summary"]
autoapi_python_class_content = "both"

viewcode_follow_imported_members = True


templates_path = []
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_logo = "images/UDS_logo_without_background.png"

html_theme_options = {
    "sticky_navigation": False,
    "collapse_navigation": False,
    "navigation_depth": 6,
}

html_static_path = []
