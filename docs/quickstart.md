# Project Set Up

In this page you will learn how to set up / work with a project using the cookiecutter. The steps are different depending on whether [you are the one setting up a project](#setting-up-a-new-project) or whether a project already exists and [you are just cloning it to set it up for yourself](#working-with-an-existing-project).

## Setting up a new project

_**Prerequisite**: If this is your first time setting up a cookiecutter project you need to install it from https://pypi.org/project/cookiecutter. You can do this in the terminal on macOS with `brew install cookiecutter`._

### 1. Set up your project locally

Open the terminal and `cd` to a folder where you eventually want your repo to be, then run the cookiecutter:

```bash
cookiecutter https://github.com/nestauk/ds-cookiecutter
```

This will automatically install the latest version. If you want to install a different version run:

```bash
cookiecutter https://github.com/nestauk/ds-cookiecutter -c <VERSION TAG>
```

You will be prompted to enter the following information:

-   `You've downloaded ~.cookiecutters/ds-cookiecutter before. Is it okay to delete and re-download it?[yes]` press Enter to confirm yes, it's always best to use the latest version.
-   `project_name [project_name]`: Enter the title of your project. This will be used in the `README.md` file and docs.
-   `module_name [project_name]`: This defaults to a sanitised (lower-case, no spaces, no numbers) version of the project name (used in `pyproject.toml` and throughout).
-   `org [nestauk]`: The GitHub organisation or user under which the repository will be created or referenced. Used to populate repository URLs in `pyproject.toml` and for `gh repo create` when `auto_configure` is set to `yes`.
-   `description [A short description of the project.]`: Add a short description
-   `openness [public]`: This determines the licence and can be changed in the future if needed, it **does not** affect the privacy setting of the GitHub repository. The options are: `public` (MIT licence) and `private` (Nesta proprietary copyright licence).
-   `venv_type [uv]`: choose how you will manage your virtual environment, the options are [`uv`](https://docs.astral.sh/uv/), [`venv`](https://docs.python.org/3/library/venv.html) or [`conda`](https://docs.conda.io/en/latest/).
-   `python_version [3.13]`: The behaviour of this prompt depends on the `venv_type` you selected. If you selected `uv` you may provide a PEP compliant expression for the `pyproject.toml` (e.g. `>=3.10`, `==3.11.*`, etc., or just `3.13`). If you selected `venv` it must be a single version that is **available** on your system (e.g. `3.10` if you have it installed). If you selected `conda`, you needn't have the version installed but again you must specify a single version (e.g. `3.10`, `3.10.2`, etc.). The `pyproject.toml` will be created with the specified version.
-   `file_structure [standard]`: choose the complexity of your project. The options are: `simple` (basic and recommended for small projects: includes folders for analysis, getters and notebooks); `standard` (a good balance between simplicity and complexity: adds folders for utils, config and pipelines; moves notebooks into analysis); and `full` (adds folders separate from the module for documentation and testing).
-   `use_r [no]`: whether you want to use R in your project. If you select `yes`, the cookiecutter will create an `renv` environment and set up some auxiliary things for the project, such as an `.Renviron` file for AWS credentials.
-   `auto_configure [yes]`: controls how much of the project configuration the cookiecutter performs automatically.
    -   `yes`: configure the project locally (venv, pre-commit, direnv, git init, initial commits on `main`/`dev`) **and** create a GitHub repo under your chosen `org` (using `gh`), pushing `main` and `dev`.
    -   `local`: configure the project locally as above but skip the GitHub remote — link a remote manually (see step 3).
    -   `no`: skip all configuration. No environment, pre-commit, `direnv`, `git init`, or GitHub remote. Run those steps yourself when ready (see [Project configuration](structure.md#project-configuration)).

### 2. Connect your local project to github

If you set `auto_configure` to `yes`, the GitHub repo has already been created and both branches pushed — you're done. If you set it to `local`, the local git repo is initialised with `main` and `dev` branches; link the remote manually by running `git remote add origin git@github.com:nestauk/<REPONAME>` to point your local project at the configured repository. Then (force) push each branch to the remote repository with, **this will overwrite anything on the remote branches**:

```bash
git checkout main
git push --set-upstream --force origin main
git checkout dev
git push --set-upstream --force origin dev
```

**Now you are all set!**

### 3. Releasing your project as a package

The `README` is pre-populated with instructions for releasing. The versioning in your package is accessible internally via `{{ cookiecutter.module_name }}.__version__` and specified in `{{ cookiecutter.module_name }}__init__.py` and externally via `pip show {{ cookiecutter.module_name }}` once installed.

## Working with an existing project

If you are a team member, you will not need to set up the project from scratch. Instead, you will clone an existing project that has already been set up.

Clone the repository and `cd` into it; you can then ascertain the `venv_type` used in the project's creation. This can be inferred by the presence of a `uv.lock` file for `uv` or an `environment.yaml` file for `conda`.

The author should then have included a `README.md` file with instructions on how to set up the project. If not, consult the documentation for the `venv_type` or ask the author for help.
