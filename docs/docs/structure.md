# Structure

This page lays out where things belong according to high-level concepts.

<!-- There is an accompanying section for each on this page in [rationale](../rationale) explaining the reasoning behind this structure, and further guides on use. -->

A direct [tree](#tree) representation of the folder hierarchy is also available.

[Example structures](../examples) will soon be available to help you structure the lower-level folders which the cookiecutter leaves to you.

_In the following sections I use `src/` to denote the project name to avoid awkward `<project_name>` placeholders._

## Project configuration - `Makefile`

We use [`make`](https://www.gnu.org/software/make/) to manage tasks relating to project setup/configuration/recurring tasks.

`make` is one of the simplest ways for managing steps that depend on each other, such as project configuration and is a common tool on Unix-based platforms.

Running `make` from the project base directory will document the commands available along with a short description.

```nohighlight
Available rules:

clean               Delete all compiled Python files 
conda-create        Create a conda environment 
conda-update        Update the conda-environment based on changes to `environment.yaml` 
docs                Build the API documentation 
docs-clean          Clean the built API documentation 
docs-open           Open the docs in the browser 
init                Fully initialise a project: install; setup github repo; setup S3 bucket 
inputs-pull         Pull `inputs/` from S3 
inputs-push         Push `inputs/` to S3 (WARNING: this may overwrite existing files!) 
install             Install a project: create conda env; install local package; setup git hooks; setup metaflow+AWS 
lint                Run flake8 linting on repository 
pip-install         Install our package and requirements in editable mode (including development dependencies) 
pre-commit          Perform pre-commit actions 
```

Where appropriate these make commands will automatically be run in the conda environment for a project.

## Git hooks

We use [pre-commit](https://pre-commit.com/) to check the integrity of git commits before they happen.

The steps are specified in `.pre-commit-config.yaml`.

Currently the steps that are taken are:

- Run the [black](https://github.com/psf/black) code autoformatter
    - This provides a consistent code style across a project and minimises messy git diffs (sometimes the code formatted by black may look "uglier" in places but this is the price we pay for having an industry standard with minimal cognitive burden)
- Check that no large files were accidentally committed
- Check that there are no merge conflict strings (e.g. `>>>>>`) lingering in files
- Fix the end of files to work across operating systems
- Trim trailing whitespace in files
- Check Toml files are well formed
- Check Yaml files are well formed
- Check we are no committing directly to `dev`, `master`, or `main`
- Run the prettier formatter (covers files such as Markdown/JSON/YAML/HTML)

**Warning:** You need to run `git commit` with your conda environment activated. This is because by default the packages used by pre-commit are installed into your project's conda environment. (note: `pre-commit install --install-hooks` will install the pre-commit hooks in the currently active environment).

In time we will be [integrating `flake8`](../roadmap#flake8) into these pre-commit hooks.
You can already lint your code using (a quite opinionated) flake8 configuration defined in `setup.cfg` by running `make lint`.

## Reproducable environment

The first step in reproducing an analysis is always reproducing the computational environment it was run in. You need the same tools, the same libraries, and the same versions to make everything play nicely together.

By listing all of your requirements in the repository you can easily track the packages needed to recreate the analysis, but what tool should we use to do that? 

Whilst popular for scientific computing and data-science, [conda](https://docs.conda.io/en/latest/) poses problems for collaboration and packaging:

- It is hard to reproduce a conda-environment across operating systems
- It is hard to make your environment "pip-installable" if your environment is fully specified by conda


### Files

Due to these difficulties, we recommend only using conda to create a virtual environment and list dependencies not available through `pip install` (one prominent example of this is `graph-tool`).

- `environment.yaml` - Defines the base conda environment and any dependencies not "pip-installable".

- `requirements.txt` - Defines the dependences required to run the code.

    If you need to add a dependency, chances are it goes here!

- `requirements_dev.txt` - Defines development dependencies.

    These are for dependencies that are needed during development but not needed to run the core code. For example, packages to build documentation, run tests, and `ipykernel` to run code in `jupyter` (It's likely that you never need to think about this file)

### Commands

- `make conda-create` - Create a conda environment from `environment.yaml` and run `make pip-install`.

    Note: this is automatically called by `make install` and `make init` but exists as a stand-alone command in case you ever need it

- `make conda-update` - Update an existing conda environment from `environment.yaml` and run `make pip-install`.
- `make pip-install` - Install our package and requirements in editable mode (including development dependencies).

### Roadmap

See [roadmap](../roadmap) for plans on improving packaging and reproducibility with [Poetry](../roadmap#Poetry) and [Docker](../roadmap#Docker).



## Secrets and configuration - `.env.*` and `src/config/*`

You _really_ don't want to leak your AWS secret key or Postgres username and password on Github. Enough said — see the [Twelve Factor App](http://12factor.net/config) principles on this point.

#### Store your secrets in a special file

Create a `.env` file in the project root folder. Thanks to the `.gitignore`, this file should never get committed into the version control repository.

 Here's an example:

```nohighlight
# example .env file
DATABASE_URL=postgres://username:password@localhost:5432/dbname
OTHER_VARIABLE=something
```

You can use [python-dotenv](https://github.com/theskumar/python-dotenv) to load the entries as follows:

```python
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # Find .env and load entries
print(os.getenv("DATABASE_URL"))
print(os.getenv("SOME_VARIABLE_NOT_IN_ENV_FILE"))
# >> postgres://username:password@localhost:5432/dbname
# >> None
```

We also have `.env.shared` which contains non-secret project configuration variables that are used for example by commands in our `Makefile`

#### Store Data-science configuration in `src/config/`

Few things scupper colloborative analysis like hard-coding hyper-parameters parameters deep in the code-base.

`src/config/base.yaml` provides a place to document choices made.

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

---

**Aside** - as well as avoiding hard-coding parameters into our code, we should **_never_** hard-code full file paths, e.g. `/home/alex/GIT/my_fantastic_data_project/outputs/data/foo.json`, this will never work on anything other than your machine.

Instead use relative paths and make use of `src.PROJECT_DIR` which will return the path to your project's base directory. This means you could specify the above path as `f"{src.PROJECT_DIR}/outputs/data/foo.json"` and have it work on everyone's machine!

---

#### Roadmap

See the [roadmap](../roadmap#Metaflow) for how `src/config` will be used to parameterise metaflow pipelines and version control their outputs.


## Data - `inputs/data`, `outputs/data`, `outputs/.cache`

Firstly, don't version control data (inputs or outputs) in git, generally you should use s3 (directly or through metaflow) to manage your data.

### `inputs/data`

Put any data dependencies of your project that your code doesn't fetch here (E.g. if someone emailed you a spreadsheet with the results of a randomised control trial).

Don't ever edit this raw data, especially not manually, and especially not in Excel. Don't overwrite your raw data. Don't save multiple versions of the raw data. Treat the data (and its format) as immutable.

Store it in [AWS S3](https://aws.amazon.com/s3/). When the project was configured, you will have been prompted for a `BUCKET` variable (now tracked in `.env.shared`). If you used the `auto_config` option, an S3 bucket will have been setup for you too.

Two make commands - `make inputs-pull` and `make inputs-push` - can be used to push and pull data from the configured s3 bucket. 

### `outputs/.cache/`


This folder is for ephemeral data and any pipeline/analysis step should be runnable following the deletion of this folder's contents.

For example, this folder could be used as a file-level cache (careful about cache invalidation!); to download a file from the web before immediately reading, transforming, and saving as a clean file in `outputs/data`; or to temporary data when prototyping.

### `outputs/data`

This folder should contain transformed/processed data that is to be used in the final analysis or is a data output of the final analysis.

Try to order this folder logically. For example, you may want subfolders organised by dataset, sections of analysis, or some other hierarchy that better captures your project.


## Fetching/loading data - `src/getters`

This folder should contain modules and functions which load our data.
Anywhere in the code base we need to load data we should do so by importing and calling a getter (except prototyping in notebooks).

This means that peppering calls like `pd.read_csv("path/to/file", sep="\t", ...)` throughout the codebase should be strictly avoided.

Following this approach means:

- If the format of `path/to/file` changes then we only have to make the change in one place
- We avoid inconsistencies such as forgetting to read a column in as a `str` instead of an `int` and thus missing leading zeroes.
- If we want to see what data is available, we have a folder in the project to go to and we let the code speak for itself as much as possible - e.g. the following is a lot more informative than an inline call to `pd.read_csv` like we had above

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

### Roadmap

On the [roadmap](../roadmap#Schema) is a speculative plan to explore the use of [pydantic](https://pydantic-docs.helpmanual.io/) to specify and validate data-schemas.

## Pipeline components - `src/pipeline`

This folder contains pipeline components. Put as much data-science as possible here.

We recommend the use of [metaflow](https://docs.metaflow.org) to write these pipeline components. 

In the coming months as we roll out [utilities and documentation to smooth out some of the rough edges of metaflow](../roadmap#Metaflow), this will become less of a recommendation and more of a stipulation.

Using metaflow:
- Gives us lightweight version control of data and models
- Gives us easy access to AWS batch computing (including GPU machines)
- Makes it easy to take data-science code into production


## Shared utilities - `src/utils`

This is a place to put utility functions needed across different parts of the codebase.

For example, this could be functions shared across different pieces of analysis or different pipelines.

### Roadmap

Over time there should be a decreasing need to add things to `utils` as we begin to develop a  [data science utilities package (`ds-utils`)](../roadmap#`ds-utils`).

## Analysis - `src/analysis`

Functionality in this folder takes the pipeline components (possibly combining them) and generates the plots/statistics to feed into reports.

It is easier to say when shomething shouldn't be in `analysis` than when something should: If one part in `analysis` depends on another, then that suggests that the thing in common is likely either a pipeline component or a shared utility (i.e. sections of `analysis` should be completely independent).

It is important that plots are persisted to disk (in `outputs/figures`).

## Notebooks

Notebook packages like [Jupyter notebook](http://jupyter.org/) are effective tools for exploratory data analysis, fast prototyping, and communicating results; however, between prototyping and communicating results code should be factored out into proper python modules.


### Where does the humble notebook live?

Notebooks should be placed as close to the place where their functionality will eventually reside as possible.

For example, if you are prototyping a "sentence transformer" pipeline then that pipeline component will likely end up somewhere like `pipeline/sentence_transformer/`, therefore you should place the notebooks for prototyping this features in `pipeline/sentence_transformer/notebooks/`.

If you're just getting started with a project and don't have a clear sense of the separation between `analysis`, `pipeline`, and `getters` yet (or it's too premature to split functionality across multiple places) then a sensible place to start is `analysis/<high-level-description>/notebooks/`.

### Version control

Since notebooks are challenging objects for source control (e.g., diffs of the `json` are often not human-readable and merging is a nightmare), we use [jupytext](https://jupytext.readthedocs.io) to pair `.ipynb` files with a human-readable and git-diffable `.py` file.

These paired `.py` files should be committed to git, `.ipynb` files are git-ignored.

To ensure jupytext works correctly you should start `jupyter` (notebook/lab) from the base directory of the project so that `jupyter` detects the `jupytext` configuration that lives in `jupytext.toml`.

### Refactoring

Everybody likes to work differently. Some like to eagerly refactor, keeping as little in notebooks as possible (or even eschewing notebooks entirely);
 where as others prefer to keep everything in notebooks until the last minute.

We do not require you to work one way or the other as long as by the time you submit a pull request (PR) for your feature everything is refactored into python modules.

Having said this, we recommended you frequently refactor the good parts - you'll thank yourself later!

A warning sign you've left it too late to refactor is if you've got duplicates of functions across the codebase rather than importing from a logical place - if it's a data preprocessing task, put it in the pipeline at `src/pipelines/<descriptive name for task>`; if it's useful utility code, refactor it to `src/utils/`; if it's loading data, refactor it to `src/getters`.

#### Tips

Add the following to your notebook (or IPython REPL):
```
%load_ext autoreload
%autoreload 2
```
Now when you save code in a python module, the notebook will automatically load in the latest changes without you having to restart the kernel, re-import the module etc.


When it comes to refactoring, open the python file [Jupytext](https://jupytext.readthedocs.io) pairs to your notebook in your editor of choice - now your notebook code is easily-readable and in the same environment you use to write python modules.

### Share with gists

As the git filter above stops the sharing of outputs directly via. the git repository, another way is needed to share the outputs of quick and dirty analysis.
We suggest using Gists, particularly the [Gist it](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/gist_it/readme.html) notebook extension which adds a button to your notebook that will instantly turn the notebook into a gist and upload it to your github (as public/private) as long.
This requires [`jupyter_nbextensions_configurator`](https://github.com/Jupyter-contrib/jupyter_nbextensions_configurator) and a [github personal access token](https://github.com/settings/tokens).

### Don't install `jupyter`/`jupyterlab` in your environment, use `ipykernel`

You should avoid `jupyter`/`jupyterlab` as a dependency in the project environment.

Instead add `ipykernel` as a dependency. This is a lightweight dependency that allows `jupyter`/`jupyterlab` installed elsewhere (e.g. your main conda environment or system installation) to run the code in your project.

The advantages of this are:

- You only have to configure `jupyter`/`jupyterlab` once
- You will save disk-space
- Faster install
- Colleagues using other editors don't have to install heavy dependencies they don't use (you wouldn't be happy if someone sent you code that depended on VScode/pycharm/spyder)

Note: `ipykernel` is also listed in `requirements_dev.txt` so you do not need to add it.


## Report - `outputs/reports`

We are currently evaluating how we report data-science work - both at the project-level and the feature-level.

Minimally, you should write reports in markdown putting them in `outputs/reports` and referencing plots in `outputs/figures`.

We are [experimenting](../roadmap#Reporting) with a toolchain using [pandoc](https://pandoc.org/) to generate HTML and PDF (LaTeX) outputs from a single ([pandoc flavoured](https://pandoc.org/MANUAL.html#pandocs-markdown)) markdown file, including facilitating the trivial inclusion of interactive [altair](https://altair-viz.github.io/index.html) plots within HTML outputs.

# Tree

```nohighlight
├── bin                              |  PROJECT CONFIGURATION SCRIPTS
│   ├── conda_activate.sh            |    Helper to activate conda in shell environment
│   ├── create_bucket.sh             |    Create S3 bucket
│   ├── create_repo.sh               |    Create Github repo
│   └── install_metaflow_aws.sh      |    Configure Metaflow with AWS
├── src                              |  PYTHON PACKAGE
│   ├── __init__.py                  |
│   ├── analysis                     |  Analysis
│   │   └── __init__.py              |
│   ├── config                       |  Configuration
│   │   ├── logging.yaml             |    logging configuration
│   │   ├── base.yaml                |    global configuration (e.g. for tracking hyper-parameters)
│   │   └── pipeline                 |    pipeline configuration files
│   │       └── .gitkeep             |
│   ├── getters                      |  Data getters
│   │   └── __init__.py              |
│   ├── pipeline                     |  Pipeline components
│   │   └── __init__.py              |
│   └── utils                        |  Utilities
│       └── __init__.py              |
├── docs                             |  DOCUMENTATION
│   ├── conf.py                      |    Configures docs
│   ├── index.rst                    |    
│   └── license.rst                  |    
├── environment.yaml                 |  CONDA ENVIRONMENT SPECIFICATION (optional component)
├── requirements.txt                 |  PYTHON DEPENDENCIES NEEDED TO RUN THE CODE
├── requirements_dev.txt             |  PYTHON DEV DEPENDENCIES (e.g. building docs/running tests)
├── inputs                           |  INPUTS (should be immutable)
│   ├── data                         |    Inputs that are data
│   ├── models                       |    Inputs that are models
│   └── README.md                    |
├── jupytext.toml                    |  JUPYTEXT CONFIGURATION
├── LICENSE                          |  
├── outputs                          |  OUTPUTS PRODUCED FROM THE PROJECT
│   ├── data                         |    Data outputs (from running our code)
│   ├── figures                      |    Figure outputs (from running our code)
│   │   └── vegalite                 |      JSON specification of altair/vegalite figures
│   ├── models                       |    Model outputs (from running our code)
│   └── reports                      |    Reports about our code and the results of running it
├── Makefile                         |  TASKS TO COORDINATE PROJECT (`make` shows available commands)
├── README.md                        |  
├── setup.py                         |  ALLOWS US TO PIP INSTALL src/
├── setup.cfg                        |  ADDITIONAL PROJECT CONFIGURATION, e.g. linting
├── .pre-commit-config.yaml          |  DEFINES CHECKS THAT MUST PASS BEFORE git commit SUCCEEDS
├── .gitignore                       |  TELLS git WHAT FILES WE DON'T WANT TO COMMIT
├── .github                          |  GITHUB CONFIGURATION
│   └── pull_request_template.md     |    Template for pull-requests (check-list of things to do)
├── .env                             |  SECRETS (never commit to git!)
├── .env.shared                      |  SHARED PROJECT CONFIGURATION VARIABLES
```
