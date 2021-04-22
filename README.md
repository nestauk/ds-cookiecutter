# Cookiecutter Data Science @ Nesta

_A logical, reasonably standardized, project structure for reproducible and collaborative pre-production data science work._

[Online documentation](http://nestauk.github.io/cookiecutter-data-science-nesta)

## Requirements to use the cookiecutter template:

- Python 3.6+
- [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0:
  ```bash
  $ pip install cookiecutter
  ```
- [poe Python package](https://github.com/nat-n/poethepoet) - for running tasks
  ```bash
  $ pip install poethepoet
  ```
- [git-crypt](https://github.com/AGWA/git-crypt) [optional - required if `auto_config` set to true (the default)] - required for metaflow on AWS
  ```bash
  $ brew install git-crypt  # mac
  $ apt-get install -y git-crypt  # Ubuntu linux:
  ```
- [github CLI](https://github.com/cli/cli) [optional - required if `auto_config` set to true (the default)] - for automatic creation and configuration of a Github repo

  - To install

    ```bash
    $ brew install gh  # mac
    ```

    Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md

  - To configure
    ```bash
    $ gh auth login  # (and follow the instructions)
    ```

## To start a new project, run:

```bash
    cookiecutter https://github.com/nestauk/cookiecutter-data-science-nesta
```
