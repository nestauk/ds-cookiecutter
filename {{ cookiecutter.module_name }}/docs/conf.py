"""Sphinx configuration."""

from datetime import datetime

project = "{{ cookiecutter.module_name }}"
copyright = f"{datetime.now().year}, Nesta"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    # "sphinx_click",
    "sphinx_rtd_theme",
]
autodoc_typehints = "description"
html_theme = "sphinx_rtd_theme"
