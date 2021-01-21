{{cookiecutter.project_name}}
==============================

{{cookiecutter.description}}

## Approach to notebooks

Jupyter notebooks are great for exploration and presentation but cause problems for working collaboratively.

Use [Jupytext](https://jupytext.readthedocs.io/en/latest/) to automatically convert notebooks to and from `.py` format, commit the `.py` version (`.ipynb` files are ignored by git).

This allows us to separate code from output data, facilitating easier re-factoring, testing, execution, and code review.
--------

<p><small>Project based on the <a target="_blank" href="https://github.com/nestauk/cookiecutter-data-science-nesta">Nesta cookiecutter data science project template</a>.</small></p>
