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

import re

with open("../../uds/__init__.py", "r", encoding="utf-8") as init_file:
    full_version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', init_file.read(), re.MULTILINE).group(1)


# -- Project information -----------------------------------------------------

project = u"UDS"
copyright = u"2021, Maciej Dąbrowski"
author = u"Maciej Dąbrowski"

# The full version, including alpha/beta/rc tags
release = full_version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = ["sphinx.ext.autodoc", "autoapi.extension"]

autodoc_typehints = "description"

autoapi_type = "python"
autoapi_dirs = ["../../uds"]
autoapi_add_toctree_entry = False


# Add any paths that contain templates here, relative to this directory.
templates_path = []

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_logo = "images/UDS_logo_without_background.PNG"

html_theme_options = {
    "sticky_navigation": False,
    "collapse_navigation": False,
    "navigation_depth": 5,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


def setup(app):
    app.add_css_file("page_width.css")
