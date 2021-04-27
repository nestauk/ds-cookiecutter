## Structure

This page lays out where things belong according to high-level concepts.

There is an accompanying section for each on this page in [rationale](rationale) explaining the reasoning behind this structure, and further guides on use.

A direct [tree](#tree) representation of the folder hierarchy is also available.

[Example structures](examples) are also available to help you structure the lower-level folders which the cookiecutter leaves to you.

### Reproducable environment

- `environment.yaml`
- `make conda-create`
- `make conda-update`
- Prefer PIP
- See [roadmap](roadmap/#poetry)

The first step in reproducing an analysis is always reproducing the computational environment it was run in. You need the same tools, the same libraries, and the same versions to make everything play nicely together.

[conda](https://docs.conda.io/en/latest/). By listing all of your requirements in the repository you can easily track the packages needed to recreate the analysis. 

If you have more complex requirements for recreating your environment, consider a virtual machine based approach such as [Docker](https://www.docker.com/).

### Secrets and configuration - `.env.*` and `src/config/*`

- `.env`
- `.env.shared`
- `src/config/`

- TODO: link to Dos and Donts
- TODO: how to use

### Data - `inputs/data`, `outputs/data`, `outputs/.cache`

- TODO: aux case
- TODO: use temporary folder (or .cache) 
- TODO:

#### `inputs/data`

Don't ever edit your raw data, especially not manually, and especially not in Excel. Don't overwrite your raw data. Don't save multiple versions of the raw data. Treat the data (and its format) as immutable. The code you write should move the raw data through a pipeline to your final analysis. You shouldn't have to run all of the steps every time you want to make a new figure (see [Analysis is a DAG](#analysis-is-a-dag)), but anyone should be able to reproduce the final products with only the code in `src` and the data in `data/raw`.

`src/fetch_data.py` should call scripts/functions to fetch all the raw data you need.

Also, if data is immutable, it doesn't need source control in the same way that code does.
Raw data should be stored with s3 [AWS S3](https://aws.amazon.com/s3/). Currently by default, we ask for an S3 bucket and use [AWS CLI](http://docs.aws.amazon.com/cli/latest/reference/s3/index.html) to sync data in the `data/raw` folder with the server.

`data/raw` is in `.gitignore` by default.

Two make commands - `make sync_data_from_s3` and `make sync_data_to_s3` - can be used to sync data to and from the configured s3 bucket (`BUCKET` in `Makefile`)

#### `outputs/.cache/`

This folder is for intermediate data that has been transformed but is not a fully processed output, perhaps as it is the output of a rough notebook.
This is up to the individual user to manage as nothing important should live here.

`data/interim` is in `.gitignore` by default.

#### `outputs/data`

This folder should contain transformed and processed data that is to be used in the final analysis or is a data output of the final analysis.

`data/processed` is in `.gitignore` by default; however if you are using DVC you may want to remove it from `.gitignore` as anything here should be version controlled with DVC+S3 (see [Data and model version control with DVC](#data-and-model-version-control-with-dvc)).


### Fetching/loading data - `getters`

TODO

### Pipeline components - `pipeline`

TODO

### Shared utilities - `utils`

TODO

TODO: mention `ds-utils`

### Notebooks

Notebook packages like [Jupyter notebook](http://jupyter.org/) are effective tools for exploratory data analysis, fast prototyping, and communicating results; however, between prototyping and communicating results code should be factored out into proper python modules.


#### Where does the humble notebook live?

TODO: put notebooks in a logical place
TODO: logical starting place is `analysis/`

Refactor the good parts (frequently). 
Don't write code to do the same task in multiple notebooks. If it's a data preprocessing task, put it in the pipeline at `src/pipelines/<descriptive name for task>`; if it's useful utility code, refactor it to `src/utils/`; if it's loading data, refactor it to `src/getters`.

Now by default we turn the project into a Python package (see the `setup.py` file). You can import your code and use it in notebooks with a cell like the following:

```
from src.data import make_dataset
```

TODO: autoreload and jupytext are your friend


#### Version control

Since notebooks are challenging objects for source control (e.g., diffs of the `json` are often not human-readable and merging is a nightmare), collaborating directly with others on Jupyter notebooks should not be attempted.


#### Share with gists

As the git filter above stops the sharing of outputs directly via. the git repository, another way is needed to share the outputs of quick and dirty analysis.
We suggest using Gists, particularly the [Gist it](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/gist_it/readme.html) notebook extension which adds a button to your notebook that will instantly turn the notebook into a gist and upload it to your github (as public/private) as long.
This requires [`jupyter_nbextensions_configurator`](https://github.com/Jupyter-contrib/jupyter_nbextensions_configurator) and a [github personal access token](https://github.com/settings/tokens).

#### Use `ipykernel`

TODO

(benefit: only have to configure extensions once)

# Tree

```nohighlight
├── bin                              |  PROJECT CONFIGURATION SCRIPTS
│   ├── conda-activate.sh            |    Helper to activate conda in shell environment
│   ├── create_bucket.sh             |    Create S3 bucket
│   ├── create_repo.sh               |    Create Github repo
│   └── install_metaflow_aws.sh      |    Configure Metaflow with AWS
├── src                              |  PYTHON PACKAGE
│   ├── __init__.py                  |
│   ├── analysis                     |  Analysis
│   │   └── __init__.py              |
│   ├── config                       |  Configuration
│   │   ├── logging.yaml             |    logging configuration
│   │   ├── model_config.yaml        |    hyper-parameter configuration
│   │   ├── .metaflow-versioning.yaml|    tracks metadata about our pipelines
│   │   └── pipeline                 |    pipeline configuration files
│   │       └── .gitkeep             |
│   ├── getters                      |  Getters
│   │   └── __init__.py              |
│   ├── pipeline                     |  Pipelines
│   │   └── __init__.py              |
│   └── utils                        |  Utilities
│       └── __init__.py              |
├── docs                             |  DOCUMENTATION
│   ├── conf.py                      |    Configures docs
│   ├── index.rst                    |    
│   └── license.rst                  |    
├── environment.yaml                 |  CONDA ENVIRONMENT SPECIFICATION
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
├── Makefile                         |  CONTAINS TASKS TO CO-ORDINATE PROJECT (run `make` to see available commands)
├── README.md                        |  
├── setup.py                         |  ALLOWS US TO PIP INSTALL src/
├── setup.cfg                        |  ADDITIONAL PROJECT CONFIGURATION, e.g. linting
├── .pre-commit-cofig.yaml           |  DEFINES CHECKS THAT MUST PASS BEFORE git commit SUCCEEDS
├── .gitignore                       |  TELLS git WHAT FILES WE DON'T WANT TO COMMIT
├── .github                          |  GITHUB CONFIGURATION
│   └── pull_request_template.md     |    Template for pull-requests (check-list of things to do)
├── .env                             |  SECRETS
├── .env.shared                      |  SHARED PROJECT CONFIGURATION VARIABLES
```
