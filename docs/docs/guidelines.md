# Managing Your Python Environment

The cookiecutter comes with built-in support to manage a project specific python (`conda`) environment via the makefile.

What is `conda`? Conda is an open-source, cross-platform package management system that makes setting up Python environments easy. It is specifically designed for data scientists and analysts.

When you run `make install`, a `conda` environment will be created for you with a name that matches the repo name. To activate it, you can run:

`conda activate <repo_name>`

For more context on how the cookiecutter creates a conda environment, click [here](https://nestauk.github.io/ds-cookiecutter/structure/). For more information on Python environments (from our Python guidelines), click [here](https://nestauk.github.io/dap_python_guidelines/python_environments.html).

Your conda environment is an encompassing python environment for your project, you can install/uninstall packages as necessary, and these will only exist in the context of the environment of your project.

To check which packages are installed in your active Conda environment, use the following command:

`conda list <repo_name>`

## Installing packages with pip

`pip` is the standard package manager for Python. It allows you to install and manage additional libraries and dependencies that are not distributed as part of the standard library.

To install a package using pip, you can use the following command:

`pip install package_name`

## The Role of a requirements.txt

A `requirements.txt` is a file commonly found in Python projects, and is generated for you as part of a cookiecutter project setup. It lists the names of all Python packages that a Python application depends on. Each line of the requirements.txt file normally contains a package name, and optionally, the version number.

Here's an example requirements.txt:

```
numpy=1.18.1
pandas=1.0.1
scikit-learn
```

If you have a `requirements.txt` file, you can install all required packages with the following command:

`pip install -r requirements.txt`

This will install the specific versions of all the packages listed in the `requirements.txt` file. This is useful for ensuring consistent environments across different systems, or when deploying a Python application.

Python’s Achilles’ heel is package dependency conflicts, so it is preferable to ensure you include package versions in your requirements.txt, to ensure that what works for you locally, works for everyone else who needs to work on the project. Not including dependencies can lead to errors for others trying to run your code, or even different results being produced, as differing versions of packages can have different functionalities.
