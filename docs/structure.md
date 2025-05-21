# Structure

This page gives a guide to where things belong within the cookiecutter structure.

A direct [tree](#tree) representation of the folder hierarchy is also given at the bottom.

Here are a couple of examples from projects:

-   [AHL - Out of Home Analysis](https://github.com/nestauk/ahl_out_of_home_analysis)

-   [AFS - Birmingham Early Years Data](https://github.com/nestauk/afs_birmingham_ey_data)

-   [ASF - Heat Pump Readiness](https://github.com/nestauk/asf_heat_pump_readiness)

-   [DS - Green Jobs](https://github.com/nestauk/dap_prinz_green_jobs)

_**Note:** In the following sections we use `src/` to denote the project name to avoid awkward `<project_name>` placeholders._

## Project configuration

Depending on your choice of `autosetup` the cookiecutter will either stop at establishing the project structure, or it will do the following for you:

1. Set up your virtual environment using your selected tool, such as `uv`, `poetry`, or `conda`.
2. Set up pre-commit and install the hooks specified in `.pre-commit-config.yaml`.
3. Run `direnv allow` in context of the project so that the `.env` and `.envrc` files are automatically loaded (importing environment variables and activating the relevant virtual environment).
4. Set up the `git` repository using `git init` and create the initial commit on `main` and `dev` branches.
5. Force push the initial commit to the remote repository (if specified) using `git push -u origin main` and `git push -u origin dev`.

These steps can be completed manually if the `autosetup` option was not used. Critically, they (with the exception of the `git` parts when cloning a repo) are the first steps we should take when working in any repository, whether it's a new project or a clone of a colleague's!

**The following sections are potentially outdated but go into greater detail about the steps above.
**

## Git hooks

We use [pre-commit](https://pre-commit.com/) to check the integrity of git commits before they happen. You should set this up with your virtual environment. With `uv`, it's as simple as adding it to the environment, sourcing the environment, and running `pre-commit install --install-hooks`.

```bash
uv add pre-commit
source .venv/bin/activate
pre-commit install --install-hooks
```

The steps are specified in `.pre-commit-config.yaml`. Some basic checks are performed on the repository (ensuring no large files commited and fixing trailing whitespace) from a [core set of pre-commit hooks](https://github.com/pre-commit/pre-commit-hooks). More critically, we use [ruff](https://docs.astral.sh/ruff/) to format and lint the repository, an all-in-one alternative to black, flake8, and isort.

Now, every time you run `git commit`, it should perform these checks automatically

**Warning:** You need to run `git commit` with your virtual environment activated. This is because by default the packages used by pre-commit are installed into your project's environment. (note: `pre-commit install --install-hooks` will install the pre-commit hooks in the currently active environment, which is why we source it before running in the example above).

## Reproducible environment

The first step in reproducing someone else’s analysis is to reproduce the computational environment it was run in. You need the same tools, the same libraries, and the same versions to make everything play nicely together.

By listing all of your requirements in the repository you can easily track the packages needed to recreate the analysis. We recommend the use of [uv](https://github.com/astral-sh/uv) to manage the requirements in your project, but you are open to choose other tools such as [poetry](https://python-poetry.org/), Python's built in venv, or [conda](https://docs.conda.io/en/latest/).

Whilst popular for scientific computing and data science, [conda](https://docs.conda.io/en/latest/) poses problems for collaboration and packaging, so we recommend moving away from its use if at all possible.

### Files

The files used to track dependencies in a virtual environment will vary based on the tool you use. For `uv` and `poetry`, the entire project will be tracked using the `pyproject.toml` file. The `pyproject.toml` file has already been pre-filled in the cookiecutter, but you should learn how it works so you can make edits and changes as necessary within your projects.

You can add or remove dependencies directly from the command line, using `uv add pandas` or `uv remove numpy` to automatically edit the `pyproject.toml` file. You can add development dependencies with the `--dev` flag like so `uv add --dev ipykernel`. You can substitute `poetry` for `uv` depending on the tool you're using.

If using `conda` or Python's built-in environment manager, you may manually manage requirements in text files, like `requirements.txt` and `requirements_dev.txt`. `conda` will also use an `environment.yaml` file to define the base conda environment and any dependencies not "pip-installable".

### Commands

You will need to create your virtual environment, install the packages, and activate it using the tool you've selected. Previously, `make install` helped with this setup and updating. Using `uv`, you can run the following:

1. `uv venv` to create a virtual environment in the `.venv` folder
2. `uv add package` to add dependencies
3. `uv sync` to ensure your virtual environment is synced with the `uv` lockfile, especially useful when entering new projects
4. `uv pip install -e .` to install the project to your environment in an editable format
5. `source .venv/bin/activate` to activate the virtual environment, or `uv run script.py` to directly run any Python script in the environment

These are just some of the commands you might want to run, if you chose `uv`. You should learn and explore whatever tool you choose so you can confidently manage your projects and its dependencies.

## Secrets and configuration - `.env.*` and `src/config/*`

You _really_ don't want to leak your AWS secret key or database username and password on Github. To avoid this you can:

#### Store your secrets in a special file

Create a `.env` file in the project root folder. Thanks to the `.gitignore`, this file should never get committed into the version control repository.

Here's an example:

```nohighlight
# example .env file
DATABASE_URL=postgres://username:password@localhost:5432/dbname
OTHER_VARIABLE=something
```

We also have `.envrc` which contains non-secret project configuration shared across users such as the bucket that our input data is stored in.

[`direnv`](https://direnv.net) automatically loads `.envrc` (which itself loads `.env`) making our configuration available. Add all environment variables directly to `.env` so they are available in Python through `dotenv` as well as in your terminal through `direnv`. You will need to activate `direnv` in the repository by running `direnv allow`.

#### Store Data science configuration in `src/config/`

If there are certain variables that are useful throughout a codebase, it is useful to store these in a single place rather than having to define them throughout the project.

`src/config/base.yaml` provides a place to document these global variables.

For example, if you were working on a fuzzy-matching the PATSTAT patent database to the Companies House database and wanted to only merge above a certain match score you may add a section to the configuration like the following,

```yaml
patstat_companies_house:
    match_threshold: 90
```

and load that value into your code with,

```python
from src import config

config["patstat_companies_house"]["match_threshold"]
```

This centralisation provides a clearer log of decisions and decreases the chance that a different match threshold gets incorrectly used somewhere else in the codebase.

Config files are also useful for storing model parameters. Storing model parameters in a config makes it much easier to test different model configurations and document and reproduce your model once it’s been trained. You can easily reference your config file to make changes and write your final documentation rather than having to dig through code. Depending on the complexity of your repository, it may make sense to create separate config files for each of your models.

For example, if training an SVM classifier you may want to test different values of the regularisation parameter ‘C’. You could create a file called
`src/config/svm_classifier.yaml` to store the parameter values in the same way as before.

---

**Note** - as well as avoiding hard-coding parameters into our code, we should **_never_** hard-code full file paths, e.g. `/home/Projects/my_fantastic_data_project/outputs/data/foo.json`, as this will never work on anything other than your machine.

Instead use relative paths and make use of `src.PROJECT_DIR` which will return the path to your project's base directory. This means you could specify the above path as `f"{src.PROJECT_DIR}/outputs/data/foo.json"` and have it work on everyone's machine!

---

## Data - `inputs/data`, `outputs/data`, `outputs/.cache`

Generally, don't version control data (inputs or outputs) in git, it is best to use s3 (directly or through metaflow) to manage your data.

### `inputs/data`

Put any data dependencies of your project that your code doesn't fetch here (E.g. if someone emailed you a spreadsheet with the results of a randomised control trial).

Don't ever edit this raw data, especially not manually or in Excel. Don't overwrite your raw data. Don't save multiple versions of the raw data. Treat the data (and its format) as immutable.

Ideally, you should store it in [AWS S3](https://aws.amazon.com/s3/). You can then use the [ds-utils](https://github.com/nestauk/ds-utils) package, which has a neat way of pulling in data into dataframe. Alternatively, if you set the `S3_INPUT_PATH` environment variable (e.g. in `.env`) then you can use `make inputs-pull` to pull data from the configured S3 bucket.

### `outputs/.cache/`

This folder is for ephemeral data and any pipeline/analysis step should be runnable following the deletion of this folder's contents.

For example, this folder could be used as a file-level cache (careful about cache invalidation!); to download a file from the web before immediately reading, transforming, and saving as a clean file in `outputs/data`; or to temporary data when prototyping.

### `outputs/data`

This folder should contain transformed/processed data that is to be used in the final analysis or is a data output of the final analysis. Again, if this data is sensitive, it is always best to save on S3 instead!

Try to order this folder logically. For example, you may want subfolders organised by dataset, sections of analysis, or some other hierarchy that better captures your project.

## Fetching/loading data - `src/getters`

This folder should contain modules and functions which load our data.
Anywhere in the code base we need to load data we should do so by importing and calling a getter (except prototyping in notebooks).

This means that lots of calls like `pd.read_csv("path/to/file", sep="\t", ...)` throughout the codebase can be avoided.

Following this approach means:

-   If the format of `path/to/file` changes then we only have to make the change in one place
-   We avoid inconsistencies such as forgetting to read a column in as a `str` instead of an `int` and thus missing leading zeros
-   If we want to see what data is available, we have a folder in the project to go to and we let the code speak for itself as much as possible - e.g. the following is a lot more informative than an inline call to `pd.read_csv` like we had above

Here are two examples:

```python
    # File: getters/companies_house.py
    """Data getters for the companies house data.

    Data source: https://download.companieshouse.gov.uk/en_output.html
    """
    import pandas as pd

    def get_sector() -> pd.DataFrame:
        """Load Companies House sector labels.

        Returns:
            Sector information for ...
        """
        return pd.read_csv("path/to/file", sep="\t", dtype={"sic_code": str})
```

or using ds-utils:

```python
    #File: getters/asq_data.py
    """Data getters for the ASQ data.
    """
    import pandas as pd
    from nesta_ds_utils.loading_saving import S3

    def get_asq_data() -> pd.DataFrame:
    """Load ASQ data for assessments taken in 2022.


    Returns: Dataframe of the ASQ data at individual level including information on …
    """
    return S3.download_obj(
        bucket="bucket_name",
        path_from="data/raw/data_asq.csv",
        download_as="dataframe",
        kwargs_reading={"engine": "python"},
    )

```

## Pipeline components - `src/pipeline`

This folder contains pipeline components. Put as much data science as possible here.

We recommend the use of [metaflow](https://docs.metaflow.org) to write these pipeline components.

Using metaflow:

-   Gives us lightweight version control of data and models
-   Gives us easy access to AWS batch computing (including GPU machines)
-   Makes it easy to take data-science code into production

## Shared utilities - `src/utils`

This is a place to put utility functions needed across different parts of the codebase.

For example, this could be functions shared across different pieces of analysis or different pipelines.

## Analysis - `src/analysis`

Functionality in this folder takes the pipeline components (possibly combining them) and generates the plots/statistics to feed into reports.

It is easier to say when shomething shouldn't be in `analysis` than when something should: If one part in `analysis` depends on another, then that suggests that the thing in common is likely either a pipeline component or a shared utility (i.e. sections of `analysis` should be completely independent).

It is important that plots are saved in `outputs/` rather than in different areas of the repository.

## Notebooks - `src/analysis/notebooks`

Notebook packages like [Quarto](https://quarto.org/) are effective tools for exploratory data analysis, fast prototyping, and communicating results; however, between prototyping and communicating results code should be factored out into proper python modules. Compared with Jupyter notebooks, Quarto `.qmd` files are Markdown based text files that render outputs to separate files, making it easier to code review the raw text and ensure sensitive outputs are not version controlled.

We have a notebooks folder for all your notebook needs! For example, if you are prototyping a "sentence transformer" you can place the notebooks for prototyping this feature in notebooks, e.g. `analysis/notebooks/sentence_transformer/` or `analysis/notebooks/pipeline/sentence_transformer/`.

Please try to keep all notebooks within this folder and primarily not on github, especially for code refactoring as the code will be elsewhere, e.g. in the pipeline. However, for collaborating, sharing and QA of analysis, you are welcome to push those to github. Make sure that you do not save rendered files (e.g. HTML) directly to GitHub.

### Refactoring

Everybody likes to work differently. Some like to eagerly refactor, keeping as little in notebooks as possible (or even eschewing notebooks entirely); whereas others prefer to keep everything in notebooks until the last minute.

You are welcome to work in whatever way you’d like, but try to always submit a pull request (PR) for your feature with everything refactored into python modules.

We often find it easiest to refactor frequently, otherwise you might get duplicates of functions across the codebase , e.g. if it's a data preprocessing task, put it in the pipeline at `src/pipelines/<descriptive name for task>`; if it's useful utility code, refactor it to `src/utils/`; if it's loading data, refactor it to `src/getters`.

#### Tips

Add the following to your notebook (or IPython REPL):

```
%load_ext autoreload
%autoreload 2
```

Now when you save code in a python module, the notebook will automatically load in the latest changes without you having to restart the kernel, re-import the module etc.

### Share with gists

As the git filter above stops the sharing of outputs directly via. the git repository, another way is needed to share the outputs of quick and dirty analysis.
We suggest using Gists, particularly the [Gist it](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/gist_it/readme.html) notebook extension which adds a button to your notebook that will instantly turn the notebook into a gist and upload it to your github (as public/private) as long.
This requires [`jupyter_nbextensions_configurator`](https://github.com/Jupyter-contrib/jupyter_nbextensions_configurator) and a [github personal access token](https://github.com/settings/tokens).

### Don't install `jupyter`/`jupyterlab` in your environment, use `ipykernel`

You should avoid `jupyter`/`jupyterlab` as a dependency in the project environment.

Instead add `ipykernel` as a dependency. This is a lightweight dependency that allows `jupyter`/`jupyterlab` installed elsewhere (e.g. your main conda environment or system installation) to run the code in your project.

Run `python -m ipykernel install --user --name=<project environment name>` from within your project environment to allow jupyter to use your project's virtual environment.

The advantages of this are:

-   You only have to configure `jupyter`/`jupyterlab` once
-   You will save disk-space
-   Faster install
-   Colleagues using other editors don't have to install heavy dependencies they don't use

**Note:** `ipykernel` is also listed in `requirements_dev.txt` so you do not need to add it.

## Report - `outputs/reports`

You can write reports in markdown and put them in `outputs/reports` and reference plots in `outputs/figures`.

# Tree

Note that this is for the `full` file structure. The `standard` and `simple` file structures are similar but with fewer folders under `<MODULE NAME>` and the omission of the `docs` and `tests` folders.

```nohighlight
.
├── <MODULE NAME>                    |  PYTHON PACKAGE
│   ├── __init__.py                  |
│   ├── analysis/                    |  Analysis
│   ├── config                       |  Configuration
│   │   ├── logging.yaml             |    logging configuration
│   │   ├── base.yaml                |    global configuration (e.g. for tracking hyper-parameters)
│   │   └── pipeline/                |    pipeline configuration files
│   ├── getters/                     |  Data getters
│   ├── notebooks/                   |  Notebooks
│   ├── pipeline/                    |  Pipeline components
│   └── utils/                       |  Utilities
├── docs/                            |  DOCUMENTATION
├── pyproject.toml                   |  PROJECT METADATA AND CONFIGURATION
├── environment.yaml                 |  CONDA ENVIRONMENT SPECIFICATION (optional component)
├── LICENSE                          |
├── outputs/                         |  OUTPUTS PRODUCED FROM THE PROJECT
├── README.md                        |
├── .pre-commit-config.yaml          |  DEFINES CHECKS THAT MUST PASS BEFORE git commit SUCCEEDS
├── .gitignore                       |  TELLS git WHAT FILES WE DON'T WANT TO COMMIT
├── .github/                         |  GITHUB CONFIGURATION
├── .env                             |  SECRETS (never commit to git!)
├── .envrc                           |  SHARED PROJECT CONFIGURATION VARIABLES
└── .cookiecutter                    |  COOKIECUTTER SETUP & CONFIGURATION (user can safely ignore)
```

## The (old) Makefile

Where did the Makefile go? Previously, our cookiecutter used a Makefile to help manage the environment and its dependencies. However, due to its growing size and complexity, it was becoming difficult to maintain. The Makefile commands were also obfuscating the underlying tools it used, preventing users from growing their experience and confidence in directly managing their project's environments.

We decided to do away with the Makefile and hope to support everyone in their journey of directly managing their projects and dependencies directly.
