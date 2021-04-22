# Cookiecutter Data Science @ Nesta

_A logical, reasonably standardized, project structure for reproducible and collaborative pre-production data science work._

Our take on the [original](https://drivendata.github.io/cookiecutter-data-science/)

#### [Project homepage (under development)](http://nestauk.github.io/cookiecutter-data-science-nesta)

### Requirements to use the cookiecutter template:

---

- Python 3.6+
- [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0: This can be installed with pip by or conda depending on how you manage your Python packages:
- Poe
- git-crypt [optional] - required for metaflow
- gh cli [optional] - if you want to automatically create a Github repo

```bash
$ pip install cookiecutter
```

or

```bash
$ conda config --add channels conda-forge
$ conda install cookiecutter
```

### To start a new project, run:

---

    cookiecutter https://github.com/nestauk/cookiecutter-data-science-nesta
