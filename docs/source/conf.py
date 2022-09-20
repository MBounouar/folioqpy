# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from importlib import metadata

project = "dash-pyfolio"
copyright = "2022, M.Bounouar"
author = "M.Bounouar"
PACKAGE_VERSION = metadata.version("dash-pyfolio")
version = PACKAGE_VERSION
release = PACKAGE_VERSION

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add napoleon to the extensions list
extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autodoc.typehints",
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
exclude_patterns = ["build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_theme = "sphinx_rtd_theme"
# html_static_path = ["_static"]


#

nitpick_ignore = [("py:class", "type")]
add_module_names = False
