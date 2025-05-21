# Project Set Up

## Your Guide to Setting Up a Nesta Cookiecutter Project

In this page you will learn how to set up a project using the cookiecutter. The steps are different depending on whether you are the first one setting up a project ([Project Configurer](#project-configuration)) or whether a project already exists and you are just setting it up locally ([Team Member](#team-members)).

### Project Configuration

_**Prerequisite**: If this is your first time setting up a cookiecutter project you need to install it from https://pypi.org/project/cookiecutter. You can do this in the terminal with `brew install cookiecutter`._

#### 1. Request repository setup

First things first, you need a repo created for you. From the [tech support website](https://nestagroup.atlassian.net/servicedesk/customer/portals), go to _Ask Nesta Technology_, _Request Forms_, then _Request GitHub repository_. You will need to provide a _project name_, _repo name_, whether _public/private_, _github teams involved_, _team leading the project_, _short and long description of the project_. An empty repo will automatically be set up for you within a few minutes: https://github.com/nestauk/your_repo_name. Your team should have admin access on the repository.

#### 2. Set up your project locally

It is important that you _do not clone the repo yet!_ Instead, open the terminal and `cd` to a folder where you eventually want your repo to be, then run the cookiecutter:

```bash
cookiecutter https://github.com/nestauk/ds-cookiecutter
```

This will automatically install the latest version. If you want to install a different version run:

```bash
cookiecutter https://github.com/nestauk/ds-cookiecutter -c <VERSION TAG>
```

You will be prompted to enter the following information:

-   `You've downloaded ~.cookiecutters/ds-cookiecutter before. Is it okay to delete and re-download it?[yes]` press Enter to confirm yes, it's always best to use the latest version.
-   `project_name [project_name]`: Enter the title of your project. This will be used in the `README.md` and `pyproject.toml` files.
-   `repo_name [project_name]`: This defaults to a sanitised version of the project name. You can change it to whatever you want, but it is recommended to keep it the same as the project name.
-   `author_name [Nesta]`: Add authors in PEP-compliant format or press Enter to confirm "Nesta"
-   `description [A short description of the project.]`: Add a short description
-   `openness [public]`: This determines the licence, this can be changed in the future if needed
-   `venv_type [uv]`: choose how you will manage your virtual environment, the options are [`uv`](https://docs.astral.sh/uv/), [`venv`](https://docs.python.org/3/library/venv.html) or [`conda`](https://docs.conda.io/en/latest/).
-   `file_structure [standard]`: choose the complexity of your project. The options are: `simple` (basic and recommended for small projects); `standard` (a good balance between simplicity and complexity); and `full` (includes folders for documentation and testing).
-   `python_version [3.10]`: the behaviour of this prompt depends on the `venv_type` you selected. If you selected `uv` you may provide a PEP compliant expression for the `pyproject.toml` (e.g. `>=3.10`, `==3.11.*`, etc.). If you selected `venv` it must be a single version available on your system (e.g. `3.10`, `3.11`, etc.). If you selected `conda`, you needn't have the version installed but again you must specify a single version (e.g. `3.10`, `3.10.2`, etc.). The `pyproject.toml` will be created with the specified version.
-   `autosetup [yes]`: this will automatically set up the project's virtual environment, pre-commit hooks and git repository for you. If you select `no`, you will have to do this manually later.'

#### 3. Connect your local project to github

You have set up your project locally and now you have to connect it to the remote repo. When you change directory to your created project folder, you will see that you are in a git repository and the generated cookiecutter has committed itself to the `main` and `dev` branches. Connect to the git repo by running `git remote add origin git@github.com:nestauk/<REPONAME>` to point your local project to the configured repository.

**Now you are all set!**

### Team Members

-   Open the terminal and `cd` into a folder where you want the project set up.
-   Clone the repository by running `git clone <REPONAME>` and `cd` into the repository.
-   Run `make install` to configure the development environment.
