# Cookiecutter Data Science @ Nesta

_A logical, reasonably standardized, project structure for reproducible and collaborative pre-production data science work._

## Disclaimers:
* The workflow and the documentation here of it are works in progress and may currently be incomplete or inconsistent in parts - please raise issues where you spot this is the case.

* The foundations of this document are heavily borrowed (large parts of it verbatim) from the great work [http://drivendata.github.io/cookiecutter-data-science/][here] by the people at [Drivendata](http://drivendata.github.io/cookiecutter-data-science/).

## High-level aims

* Shouldn’t get in the way of rapid prototyping of ideas for an individual
* Analysis of one user should be runnable and reproducable by another user without changes
* Minimal computation and data transfer when rerunning the pipeline after changes
* Long-term integrity of the code-base without intervention
* Version control for data, models, outputs/metrics
* Reduce time to productionise analysis

## Getting started

While this template focuses on Python, the general project structure can be used with another language after removing the Python boilerplate in the repo such as the the files in the `src` (***note*** that `src` will actually be named the same as your repo name) folder, and the Sphinx documentation skeleton in `docs`).

### Requirements

 - Python 3.6+
 - [cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0: `pip install cookiecutter`
 - A *NIX system (e.g. Linux/OSX) is required to ensure full functionality.


### Starting a new project

Starting a new project is as easy as running this command at the command line. No need to create a directory first, the cookiecutter will do it for you.

```nohighlight
cookiecutter https://github.com/nestauk/cookiecutter-data-science-nesta
```

For getting started quickly, have a look at the [quickstart](quickstart.md) or [FAQ](faq.md).

### Reproducing analysis for an existing project

If the project structure has been adhered to and an appropriate `Makefile` entry made then reproducing the analysis should be a one-liner (assuming your `.env` contains everything it needs to - nothing by default).

```nohighlight
make all
```

## Structure

```
    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── README.md      <- An inventory of data-sources, including schemas (or links to schemas)
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   ├── aux            <- Non-automatable human interventions, e.g. hand selected record ID's to ignore
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── logging.yaml       <- Logging config
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── model_config.yaml  <- Model configuration parameters
    │
    ├── notebooks          <- Jupyter notebooks. Notebooks at the top level should have a markdown header
    │   │                     outlining the notebook and should avoid function calls in favour of factored out code.
    │   │                     
    │   ├── notebook_preamble.ipy
    │   │                     
    │   └── dev            <- Development notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `_` delimited description, e.g.
    │                         `01_jmg_eda.ipynb`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   ├── eda            <- Generated exploratory data analysis reports
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── conda_environment.yaml <- A reproducable conda environment.
    │                             installable with `conda env create -f conda_environment.yaml`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so {{ cookiecutter.repo_name }} can be imported
    │
    ├── {{ cookiecutter.repo_name }}                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes {{ cookiecutter.repo_name }} a Python module
    │   │
    │   ├── fetch_data.py  <- Script to fetch data into data/raw
    │   │
    │   ├── make_dataset.py<- Scripts to generate processed data
    │   │
    │   ├── transformers   <- Methods that perform `transform` on a dataset but not `fit` (or pre-trained models)
    │   │
    │   ├── estimators     <- Methods that perform `fit` on a dataset
    │   │
    │   └── visualisation  <- Scripts to create exploratory and results oriented visualisations
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org
```

### Overview



### Analysis is a DAG

Often in an analysis you have long-running steps that preprocess data or train models. If these steps have been run already, you don't want to wait to rerun them every time.
[`make`](https://www.gnu.org/software/make/) is one of the simplest ways for managing steps that depend on each other, especially the long-running ones. Make is a common tool on Unix-based platforms. Following the [`make` documentation](https://www.gnu.org/software/make/), [Makefile conventions](https://www.gnu.org/prep/standards/html_node/Makefile-Conventions.html#Makefile-Conventions), and [portability guide](http://www.gnu.org/savannah-checkouts/gnu/autoconf/manual/autoconf-2.69/html_node/Portable-Make.html#Portable-Make) will help ensure your Makefiles work effectively across systems. Here are [some](http://zmjones.com/make/) [examples](http://blog.kaggle.com/2012/10/15/make-for-data-scientists/) to [get started](https://web.archive.org/web/20150206054212/http://www.bioinformaticszen.com/post/decomplected-workflows-makefiles/). A number of data folks use `make` as their tool of choice, including [Mike Bostock](https://bost.ocks.org/mike/make/).

There are other tools for managing DAGs that are written in Python instead of a DSL (e.g., [Luigi](http://luigi.readthedocs.org/en/stable/index.html) which is used in [Nesta's production system](https://github.com/nestauk/nesta/tree/dev/nesta/production)) - though these generally impose more constraints which can slow down the prototyping stage.

While `make` is good for managing quick, and simple steps rerunning a complicated DAG may take a large amount of time to perform when perhaps only the last stage has actually changed. Of course, one could only run the last stage but how do you know with certainty that no other long lived stage has changed since you last ran it?

This is why we need data and model version control (see [DVC](#data-and-model-version-control-with-dvc)).

Several generic `make` commands are made [available](make_commands) within the cookiecutter for performing certain tasks.

### Build from the environment up

The first step in reproducing an analysis is always reproducing the computational environment it was run in. You need the same tools, the same libraries, and the same versions to make everything play nicely together.

One effective approach to this is use [conda](https://docs.conda.io/en/latest/). By listing all of your requirements in the repository (we include a `conda_environment.yaml` file) you can easily track the packages needed to recreate the analysis. Here is a good workflow:

 1. Add any required dependencies to `conda_environment.yaml`
 2. Run `make create_environment` to create an environment with the required dependencies
 3. Add dependencies to `conda_environment.yaml` as you go so that others can reproduce your environment

If you have more complex requirements for recreating your environment, consider a virtual machine based approach such as [Docker](https://www.docker.com/) or [Vagrant](https://www.vagrantup.com/). Both of these tools use text-based formats (Dockerfile and Vagrantfile respectively) you can easily add to source control to describe how to create a virtual machine with the requirements you need.

### Keep secrets and configuration out of version control

You _really_ don't want to leak your AWS secret key or Postgres username and password on Github. Enough said — see the [Twelve Factor App](http://12factor.net/config) principles on this point. Here's one way to do this:

#### Store your secrets and config variables in a special file

Create a `.env` file in the project root folder. Thanks to the `.gitignore`, this file should never get committed into the version control repository. Here's an example:

```nohighlight
# example .env file
DATABASE_URL=postgres://username:password@localhost:5432/dbname
AWS_ACCESS_KEY=myaccesskey
AWS_SECRET_ACCESS_KEY=mysecretkey
OTHER_VARIABLE=something
```

#### Use a package to load these variables automatically.

If you look at the stub script in `src/data/make_dataset.py`, it uses a package called [python-dotenv](https://github.com/theskumar/python-dotenv) to load up all the entries in this file as environment variables so they are accessible with `os.environ.get`. Here's an example snippet adapted from the `python-dotenv` documentation:

```python
# src/data/dotenv_example.py
import os
from dotenv import load_dotenv, find_dotenv

# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()

# load up the entries as environment variables
load_dotenv(dotenv_path)

database_url = os.environ.get("DATABASE_URL")
other_variable = os.environ.get("OTHER_VARIABLE")
```

#### AWS CLI configuration
When using Amazon S3 to store data, a simple method of managing AWS access is to set your access keys to environment variables. However, managing mutiple sets of keys on a single machine (e.g. when working on multiple projects) it is best to use a [credentials file](https://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html), typically located in `~/.aws/credentials`. A typical file might look like:
```
[default]
aws_access_key_id=myaccesskey
aws_secret_access_key=mysecretkey

[another_project]
aws_access_key_id=myprojectaccesskey
aws_secret_access_key=myprojectsecretkey
```
You can add the profile name when initialising a project; assuming no applicable environment variables are set, the profile credentials will be used be default.


### Data folder

#### `data/raw`

Don't ever edit your raw data, especially not manually, and especially not in Excel. Don't overwrite your raw data. Don't save multiple versions of the raw data. Treat the data (and its format) as immutable. The code you write should move the raw data through a pipeline to your final analysis. You shouldn't have to run all of the steps every time you want to make a new figure (see [Analysis is a DAG](#analysis-is-a-dag)), but anyone should be able to reproduce the final products with only the code in `src` and the data in `data/raw`.

`src/fetch_data.py` should call scripts/functions to fetch all the raw data you need.

Also, if data is immutable, it doesn't need source control in the same way that code does. 
Raw data should be stored with s3 [AWS S3](https://aws.amazon.com/s3/). Currently by default, we ask for an S3 bucket and use [AWS CLI](http://docs.aws.amazon.com/cli/latest/reference/s3/index.html) to sync data in the `data/raw` folder with the server.

`data/raw` is in `.gitignore` by default.

Two make commands - `make sync_data_from_s3` and `make sync_data_to_s3` - can be used to sync data to and from the configured s3 bucket (`BUCKET` in `Makefile`)

#### `data/interim`

This folder is for intermediate data that has been transformed but is not a fully processed output, perhaps as it is the output of a rough notebook.
This is up to the individual user to manage as nothing important should live here.

`data/interim` is in `.gitignore` by default.

#### `data/aux`

Some analyses may not be runnable from start to finish without human intervention, these "hand-written" datasets should be stored in `data/aux` and tracked in git. For example, clusters for unsupervised learning may need to be labelled or certain rows of a dataset dropped after manual inspection. ***For this reason it is important that analyses are exactly reproducable where possible as if clusters change then so will their label indices (see [seeds and workers](#no-hard-coding))***. 

#### `data/processed`

This folder should contain transformed and processed data that is to be used in the final analysis or is a data output of the final analysis.

`data/processed` is in `.gitignore` by default; however if you are using DVC you may want to remove it from `.gitignore` as anything here should be version controlled with DVC+S3 (see [Data and model version control with DVC](#data-and-model-version-control-with-dvc)).


### Data and model version control with DVC

[DVC](https://dvc.org) is an open-source version control system for Machine Learning Projects designed to make models and data shareable and reproducible.

![](https://dvc.org/static/img/flow-large.png)

[Short](https://dvc.org/doc/get-started) and [long](https://dvc.org/doc/tutorial) tutorials are available within their documentation.
 An example tutorial specific to this cookiecutter is being developed (see [Tutorial](#tutorial)).

#### Brief overview

DVC integrates with and works very similar to git, for example:

* `dvc add images` tracks a file just like `git add`
* `dvc remote add myrepo s3://mybucket` adds a remote just like `git remote add`
* `dvc push` pushes changes just like `git push`

DVC also allows the expression of DAG's. `dvc run -f cnn.dvc -d images -o model cnn.py` generates a `cnn.dvc` file which contains MD5 hashes for each of the dependencies (`images`), outputs (`model`), and the file which is executed (`cnn.py`) along with the dependency information.

The dependencies and outputs will be stored in the DVC cache, while `cnn.dvc` can be tracked by Git to link the given model output to the current commit.

Running `dvc repro cnn.dvc** will reproduce this step, and if the current hashes exist in the DVC cache then no work will be done which may save re-running expensive training steps when sharing a repository.

**We are currently working on incorporating DVC into the cookiecutter**

### Notebooks

Notebook packages like [Jupyter notebook](http://jupyter.org/) are effective tools for exploratory data analysis, fast prototyping, and communicating results; however, they can pose challenges when reproducing an analysis and when trying to track changes with git. 

Since notebooks are challenging objects for source control (e.g., diffs of the `json` are often not human-readable and merging is a nightmare), collaborating directly with others on Jupyter notebooks should not be attempted.

#### Naming

Follow a naming convention that shows the owner and the order the analysis was done in. We use the format `<step>_<initials>_<description>.ipynb` (e.g., `01_jmg_eda.ipynb`).

#### Refactoring

Refactor the good parts (frequently). Don't write code to do the same task in multiple notebooks. If it's a data preprocessing task, put it in the pipeline at `src/make_dataset.py`. If it's useful utility code, refactor it to `src`. 

Now by default we turn the project into a Python package (see the `setup.py` file). You can import your code and use it in notebooks with a cell like the following:

```
from src.data import make_dataset
```

#### Reducing boilerplate

The first cell of most notebooks look mostly the same: a lot of library imports, a few IPython magic commands, and a few variable definitions. This can be simplified by factoring out the common parts into a `notebooks/notebook_preamble.ipy` file which can be run at the top of a notebook as follows:

```
%run notebook_preamble.ipy
```

This provides a few pieces of functionality:

* Sets matplotlib to inline
* Loads the autoreload extension and configures it such that changes from `src` will immediately be re-imported into the notebook
* Imports core python scientific stack (numpy/scipy/pandas/matplotlib)
* Defines `project_dir` and `data_path` variables to avoid hard-coded paths
* Sets up logging to log both within the notebook and to `notebooks.log`

#### Git filter

As mentioned above, source control with notebooks is tricky. One way to increase the readability of `diff`'s is to use a Git filter to strip notebooks of their output before performing any action with git.

This is done using a short [jq](https://stedolan.github.io/jq/) command. The git filter is automatically installed to `.git/config` and `.gitattributes` when starting a cookiecutter project, but anyone cloning/forking the repository will need to install the filter manually by running `make git`.

#### Share with gists

As the git filter above stops the sharing of outputs directly via. the git repository, another way is needed to share the outputs of quick and dirty analysis.
We suggest using Gists, particularly the [Gist it](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/gist_it/readme.html) notebook extension which adds a button to your notebook that will instantly turn the notebook into a gist and upload it to your github (as public/private) as long.
This requires [`jupyter_nbextensions_configurator`](https://github.com/Jupyter-contrib/jupyter_nbextensions_configurator) and a [github personal access token](https://github.com/settings/tokens).



### Git

There are many different ways to use Git each with their pros and cons, refer to your organisations workflow (Nesta members can find ours in the [playbook](https://github.com/nestauk/imt_playbook)).

### Style and Documentation

#### PEP8

Basic [PEP8](https://www.python.org/dev/peps/pep-0008/) and style requirements apply.

The `make lint` command can be used to use `black` to format code.

Code formatting can be heavily opinion based with much debate over things such as linelengths etc.
We recommend the use of [`black`](https://black.readthedocs.io/en/stable/) which gives fast, deterministic code-formatting that avoids wasting mental energy of worrying about code formatting and improves code review speed by formatting code in a way that produces smaller diffs. It is convenient to run from the command line or incorporate into your favourite [editor](https://black.readthedocs.io/en/stable/editor_integration.html).

#### Doc-strings

[Google doc-strings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) should be written for every exposable function/class.

In addition, it is proposed to add a `#UTILS` flag at the end of a docstring for functions/classes that should be put into a utilities package for re-use across projects and subject to more rigorous testing and standardisation.

#### Data README

`data/README.md` should document everything in `data/{raw,aux,processed}`. For example

```
# raw

## something_from_online.xlsx

<Details about what the file contains>

Obtained via `wget` by running `make fetch`

### Columns

<column name 0> : <brief description>
      ...
<column name N> : <brief description>

# aux

## drop_ids.txt

Contains one id corresponding to <column name 0> in 
`raw/something_from_online.xlsx` per line which 
should be dropped due to formatting errors.

# processed

## processed_dataset.csv

Cleaned and processed version of `data/raw/something_from_online.xlsx`.

Produced by running `make data`

### Columns

<column name 0> : <brief description>
      ...
<column name N> : <brief description>
```

#### Logging

`logging` module should be used over `print` statements. There are multiple reasons for this such as the ability to log severity levels, use timestamps, and know the origin of a log message.

The [Logging cookbook](https://docs.python.org/3/howto/logging-cookbook.html) is a good resource to understand how the `logging` module works but the cookiecutter is setup such that logging is setup with a good default using both [`logging.yaml`](https://github.com/nestauk/cookiecutter-data-science-nesta/blob/master/%7B%7B%20cookiecutter.repo_name%20%7D%7D/logging.yaml) and [`src/__init__.py`](https://github.com/nestauk/cookiecutter-data-science-nesta/blob/master/%7B%7B%20cookiecutter.repo_name%20%7D%7D/%7B%7B%20cookiecutter.repo_name%20%7D%7D/__init__.py).

In order to setup logging to both `stdout`/`stderr` and to `info.log` and `errors.log` all one needs to do is import the `src` repository and initalise a logger object:

```python
import <repo_name>
import logging

logger = logging.getLogger(__name__)
logger.info('Logs at INFO level to info.log')
logger.info('Logs at ERROR level to errors.log')
```

### No hard-coding

Few things scupper colloborative analysis like hard-coding configuration parameters deep in the code-base. Where possible we believe that data/configuration and code should remain separate.
Several different entities can end up being buried in code for which we provide a solution to avoiding.

#### Paths

Hard-coding paths to data - e.g. `"/home/nesta/project/data/raw/file.csv" - means that everytime someone wishes to run your analysis they have to find every path and correct it to their system. Furthermore, if there are several contributors to a repository then different users paths will cause a lot of unneccessary diff's at best and a lot of merge conflicts to resolve at worst.

For this reason ***never*** hard-code a folder path. Use the `<repo_name>.project_dir` variable to refer to paths, e.g. `f'{project_dir}/data/raw/file.csv'`. 

For some analyses you may be using the same raw data across multiple projects and not have the disk space to store multiple copies in the respective [`data/raw`](#data-folder) folders.
Rather than reference a hard-coded external directory (e.g. `/storage/file.csv`), one should create a [symlink](https://www.unixtutorial.org/unix-symlink-example) from both `data/raw` folders pointing to the external directory such that `f'{project_dir}/data/raw/file.csv'` will actually reference `/storage/file.csv` without requiring the data to be stored multiple times.

#### Parameters

A data science project typically involves at least several dozen decisions on what thresholds, hyper-parameters etc. to use which if buried in the code-base will never be on the radar of someone who didn't write the code and is often forgotten even by the person who wrote it!

Tracking these choices in `model_config.yaml` gives these high visibility and makes the analysis more transparent. YAML is easy to read, [easy to write](https://learnxinyminutes.com/docs/yaml/), and easy to load:

```python
import yaml
fname = f'{project_dir}/model_config.yaml'
with open(fname, 'r') as f:
    params = yaml.safe_load(f)
```

For convenience, we've set it up so you can use `import <repo_name>; <repo_name>.config` to access your YAML config.

Alternatively, you may wish to use your favourite configuration parser.

#### Seeds and workers

Pseudo-random number generation (PRNG) lies at the core of many of the bread and butter data science techniques, and it is therefore important to keep track of the seeds used for each analysis to ensure that results are as exactly reproducible as possible across runs.
This can be done by setting the seeds for the PRNG's used at the start of any analysis by using `numpy.random.seed(0)` and `random.seed(0)`. ***Note:*** avoid calling this at multiple points throughout the code as re-seeding the PRNG will cause the same numbers to be drawn again in the same order.

Certain algorithms such as [Gensim's Word2Vec](https://radimrehurek.com/gensim/models/word2vec.html) implementation use Python's built-in hash-function which is [seeded by the environment variable `PYTHONHASHSEED`](https://docs.python.org/3.7/using/cmdline.html#miscellaneous-options) meaning that the environment variable needs to be set with `export PYTHONHASHSEED=0` to ensure reproducibility.

Finally, another consideration is the number of threads/cores to use for analysis and to make this easy configurable. Different users may have different computational resources available to them and may opt to run on more or fewer cores. Furthermore, this choice may affect reproducibility as many multi-threaded algorithms are not exactly reproducible due to OS thread scheduling therefore if exact reproducibility is necessary then only one worker should be used.

## Cookiecutter in practice

A [tutorial](tutorial.md) outline has been developed and will be collaboratively updated as we adopt this new way of working. The tutorial outlines how this project structure works in practice end-to-end for a simple analysis of the Gateway to Research data trying to predict which UK research council funded a research proposal based on its abstract.
NOTE: This is currently incomplete and slightly out of date.

## Roadmap

* Add an option to configure the cookiecutter to make easier use of DVC

* [`data_getters.labs`](https://github.com/nestauk/data_getters/issues/6)
  If the need to share an analysis adhering to this workflow across repositories arises, this generally suggests that it should probably be put into the production system; however this might not be possible to do quickly, or may be slightly premature.
  In this case, outputs to share should be pushed to the s3 `nesta-data-getters` and a thin wrapper function added to the `labs` subpackage of `data_getters` that fetches this data, and signposts to the original analysis. 
  `labs` will be periodically reviewed to asssess whether components should be productionised or deprecated.
  
* Plans to outline and implement a procedure for factoring out `#UTILS` functions into [nesta.packages](https://github.com/nestauk/nesta/nesta/packages)

* Code review guidelines

* Testing 
  A guide for how to write tests for Data science code will be developed and testing requirements will be phased which will require a given level of testing for *all* code, data, models that are used as a component of *any* analysis which is exposed beyond the developers team.


* Plotting style
  Consistent visual grammar of graphics to produce consistent high quality plots for various outputs (papers, blogs, reports, presentations etc.).

* EDA framework
  A guide to performing EDA on a new dataset and producing a summary report of the output - this would also assist in the data auditing process (see the Nesta [blog](https://www.nesta.org.uk/blog/red-lines-grey-area/)).

## Thanks

Finally, a thanks to [Drivendata](http://drivendata.github.io/cookiecutter-data-science/) and the [Cookiecutter](https://cookiecutter.readthedocs.org/en/latest/) project ([github](https://github.com/audreyr/cookiecutter)).
