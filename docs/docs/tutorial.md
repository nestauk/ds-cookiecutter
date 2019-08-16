<span style="color:red"><b>NOTE TO NON-NESTA VISITORS</b>: This tutorial is incomplete </span>
# Introduction

In this tutorial we are going to cover the workflow for creating a supervised model. In this instance, we will train a classifier to predict the name of the body who funded a research project from Gateway to Research based on its abstract text.

The main aims of this tutorial are to learn how to structure the repository, prototype, and factor out code into modules so that the model and any processed data can be reproduced by anyone else with a simple command.

In this tutorial, we will:

1.  Collect raw data from MySQL
2.  Explore the data in a notebook
3.  Write a data README
4.  Clean and preprocess the data
5.  Factor out cleaning and preprocessing code into modules
6.  Prototype feature extraction and model in a notebook
7.  Train and save the modelling pipeline
8.  Factor out feature extraction and modelling code into modules
9.  Put model and data under version control
10. Update model
<!-- 11. Create a publishable analysis notebook -->

Along the way, we should also keep a lab book, to document what we’ve been doing.

# The Repository

To begin with, clone the repository into a directory on your machine with the `git clone` command:

    $ git clone https://github.com/nestauk/baking-cookies.git
    $ # OR: git clone git@github.com:nestauk/baking-cookies.git

Move in to the repository directory:

    $ cd baking-cookies

If you type `git branch`, you can see that you are on the `master` branch. In general, we want to maintain the master branch for completely finished work, so we will work from the `dev` branch instead (within the settings for a Github repository you can change the default branch from `master` if you wish).

    $ git checkout dev

From `dev` we will create two more branches. One will be for the sub-project - creating our model - and another will be your personal branch for work in progress (WIP).
We make this second one because it is possible that both you and someone else will be prototyping for this sub-project at the same time, and it will be better if you have separate spaces to do this.
For example, this allows you to backup your work by pushing to the remote without worrying about someone else pulling in those changes. 
**Do not use someone else's personal branch** : personal branches are liable to be deleted/rebased/make breaking changes.

Use the `-b` flag to create and checkout your new branches simultaneously. I’m going to use my initials ("gr") for the second branch, but you can use your own if you prefer.

    $ git checkout -b gtr-predict-funder
    $ git checkout -b gtr-predict-funder-gr-wip

On your personal branch, you can prototype in notebooks that aren’t intended for mass readership (though you may still want to make them readable enough to show collaborators).
This is where we will work until we’re ready to write more polished code and produce models.

While we’re getting set up, we should install the repository package in to the Python environment you want to use.

    $ pip install -e .

We recommend (disk space permitting) that you have one environment per project. You can initialise a new conda environment by running `make create_environment`, and install the environment requirements in `conda_environment.yaml` with `make requirements`.
When adding requirements to `conda_environment.yaml` only add the major dependencies (e.g. `pandas` not everything it depends on), and do not restrict the version numbers too much (e.g. `- pandas=0.24.2` rather than `- pandas=0.24.2=py37he6710b0_0`) - this will avoid difficulties with other people on different operating systems not being able to reproduce your environment.


# Loading, Cleaning and Preprocessing

You might have noticed that there is a `notebooks` folder in the project root directory.
In here, there is a subdirectory, `dev`. This folder is for any notebooks that can be considered work in progress. See our [guide to using notebooks](https://nestauk.github.io/cookiecutter-data-science-nesta/#notebooks).

Launch jupyter and create a notebook in `notebooks/dev/` for cleaning and processing the data. With our naming convention in mind, we will call this notebook [`01_gr_gtr_projects`](https://github.com/nestauk/baking-cookies/blob/gtr-projects/notebooks/dev/01_gr_gtr_projects.ipynb).


## Loading

The data we need for this tutorial is on Nesta’s MySQL database.
From the screenshot below you can see how we will write some simple code to grab the table we need, but there are also a few important things to note:

1.  The first cell in the notebook magic runs the preamble script. This loads some useful data science libraries and runs some useful boilerplate code so that we can quickly access variables such as the project directory. You can adapt this script to your project’s needs.
2.  We hard code `config_path` to point to the location of our database config file. This is fine for now because we are working in a notebook that no one else is expected to be able to run seamlessly, but we will change it later.
3.  After collecting the data, we show the head of the dataframe. Printing and showing outputs at stages along the prototyping should be standard practice so that if you do show someone else the notebook, they can easily see what’s going on, without needing to run the code.
    
    ![img](DS_workflow_tutorial_-__Nesta_Cookie_Cutter_Basic_ML_Tutorial/screenshot_2019-08-13_14-44-14.png)

After loading and inspecting the data we will add another cell that saves it locally as a flat file to our `raw` directory.

    projects.to_csv(f'{data_path}/raw/gtr_projects.csv', index=False)


<a id="orgfd3d6e7"></a>

## EDA

All new data should be explored before it is worked with in any serious capacity.
**NOTE**: The EDA in this tutorial is not very rigorous. More rigorous guidelines for EDA are on the [roadmap](https://nestauk.github.io/cookiecutter-data-science-nesta/#roadmap). This section of the tutorial will be updated accordingly in the future.

Here we will use `pandas_profiling` and some more specific exploration. If you don’t have it you can easily install it with

    $ pip install pandas-profiling

The profiler produces a standard output, and covers many data quality elements.
It’s likely to be useful for anyone else looking at this dataset, so we will also save it in the `reports` directory as a html file.

![img](DS_workflow_tutorial_-__Nesta_Cookie_Cutter_Basic_ML_Tutorial/screenshot_2019-08-13_14-48-04.png)

Now we can dive in to the specific features that we’re interested in. First we look at the distribution of funders.

![img](DS_workflow_tutorial_-__Nesta_Cookie_Cutter_Basic_ML_Tutorial/screenshot_2019-08-13_14-48-26.png)
It looks like we have fairly good representation from all of the funders, with over 5,000 projects for each of them apart from NC3Rs. 

Let’s also look at the distribution of abstract text lengths.

![img](DS_workflow_tutorial_-__Nesta_Cookie_Cutter_Basic_ML_Tutorial/screenshot_2019-08-13_14-49-05.png)
There’s a peak at around 4,000 characters which presumably relates to a length limitation imposed on submitted abstracts. However, there’s also a peak close to 0. Let’s take a look at the distributions by funder and also have a closer look at that low end.

![img](DS_workflow_tutorial_-__Nesta_Cookie_Cutter_Basic_ML_Tutorial/screenshot_2019-08-13_14-49-22.png)

![img](DS_workflow_tutorial_-__Nesta_Cookie_Cutter_Basic_ML_Tutorial/screenshot_2019-08-13_14-49-32.png)
It looks like there’s some projects with very few characters which we will probably discard. However, there are a high frequency of abstracts with lengths at around 250 and 350 characters. Does this correspond to another word limit, or is there something else happening?

We can print out the highest frequency texts for each funder:

![img](DS_workflow_tutorial_-__Nesta_Cookie_Cutter_Basic_ML_Tutorial/screenshot_2019-08-13_14-50-00.png)
It’s pretty clear that there is some placeholder text that is repeated many times throughout the dataset.


## Cleaning

From all of this information, we can make some decisions about data cleaning:

1.  Drop all projects with abstracts that have fewer than 150 characters
2.  Drop projects where the abstract matches any of the placeholder texts
3.  For good measure, we will also drop all but one of any duplicate abstracts

Step 2 is an example of where we will use the [`aux` data folder](https://nestauk.github.io/cookiecutter-data-science-nesta/#data-folder). This is reserved for small pieces of information that have been manually created and are used in any preprocessing, analysis or modelling. In this case, we will save the two abstracts in a `.txt` file.

![img](DS_workflow_tutorial_-__Nesta_Cookie_Cutter_Basic_ML_Tutorial/screenshot_2019-08-13_14-52-01.png)

Now we can prototype our cleaning function in the notebook and test it on the dataframe.

![img](DS_workflow_tutorial_-__Nesta_Cookie_Cutter_Basic_ML_Tutorial/screenshot_2019-08-13_14-52-20.png)
    Looks good.

## Pre-processing

The last step is to prepare our abstracts for modelling by cleaning and tokenizing the raw text.

To do that, copy and paste [this chunk of code](https://gist.github.com/georgerichardson/bbde2b4a5cdde7fedd24d3d157db5ca5) below into a cell and run it.

Finally, we can check that this works by applying it to the text.

![img](DS_workflow_tutorial_-__Nesta_Cookie_Cutter_Basic_ML_Tutorial/screenshot_2019-08-13_14-53-31.png)

Looks good. From here we’re ready to take our first step to factoring out our code into a more reproducible and shareable form.

After exploration and writing cleaning functions, we need to preprocess the text.


<a id="org703e9a6"></a>

## ⏸ Pause - Lab Book

Remember near the beginning, we said we would keep a lab book of what we were doing?
So far we’ve just been forging ahead with coding. That’s great, but before we go too far, we should record what we’ve done.

A lab book is a personal thing and it's up to you how you keep it whether it be paper, google docs, markdown etc.
What is most important is that you keep one. Write down what you tried (even if it failed), references to useful blogs/papers, fixes to bugs/install issues, and issues in the data you discover as you go.
We suggest that you review your lab-book regularly, e.g. daily or weekly, and add information relevant to others as issues/comments on an issue. 
One particularly important thing to document in a common issue thread are any outliers/issues/odd entries in a dataset.

## Refactoring

Now at the end of the `make_dataset` stage (before we apply/train any models to generate features).

Here we factor out our functions from our notebooks, write any docstrings necessary, update data Readme's etc.


<a id="org4e7f088"></a>

### [`data/README.md`](https://github.com/nestauk/baking-cookies/blob/gtr-projects/data/README.md)

Write the [data Readme](https://nestauk.github.io/cookiecutter-data-science-nesta/#style-and-documentation).


<a id="org90b413c"></a>

### [`baking_cookies/data/make_dataset.py`](https://github.com/nestauk/baking-cookies/blob/gtr-projects/baking_cookies/data/make_dataset.py)

-   Write a function which collects or reads the raw data
-   `.env` file points to config location of the MySQL config file
-   Also use `model_config.yaml` which is tracked to get parameters for data processing

### [`baking_cookies/data/sql.py`](https://github.com/nestauk/baking-cookies/blob/gtr-projects/baking_cookies/data/sql.py)

Put our generic `get_engine` function here and add a [`#UTILS` flag](https://nestauk.github.io/cookiecutter-data-science-nesta/#style-and-documentation) to the docstring as this is a reusable component that we don't wish to keep repeating across repositories.


### [`baking_cookies/data/make_gtr.py`](https://github.com/nestauk/baking-cookies/blob/gtr-projects/baking_cookies/data/gtr.py)

-   Factor out the data processing functions from the notebook
-   Defines file in and file out
-   Loads in any `aux` data

### [`baking_cookies/features/text_preprocessing.py`](https://github.com/nestauk/baking-cookies/blob/gtr-projects/baking_cookies/features/text_preprocessing.py)

-   Generic functions for text preprocessing that might be applied to other data too
-   Add `#UTILS` flag

This is a good point to make a PR. Add someone to review.
In the mean time you can get on with other tasks etc. (put “closes #<issue number>” in commit message) 

### **Guidelines**

We have a few guidelines to suggest how you should structure files. 
If you find these are not sensible for your use-case please report this on this [issue](https://github.com/nestauk/cookiecutter-data-science-nesta/issues/29).

-   Segregate functions into files/folders based on functionality and then dataset where possible.
    You might want to put functionality relating to: data in `baking_cookies/data`; functionality that produces features in `baking_cookies/features`; functionality that produces models in `baking_cookies/models`.
-   Each high-level component (e.g. the creation of the cleaned and pre-processed Gateway to Research dataset) should be callable in one function with a prefix `make_` that accepts paths and parameters as arguments. 
    
    -   `make_` functions should perform any necessary setup IO work (e.g. read data from disk), call a function with a `process_` prefix, then perform any necessary IO tear-down work (e.g. save data to disk).
    -   `process_` functions should accept data and parameters (i.e. not paths) and return data - they should not perform IO!
    
    It may not always be possible to adhere to this pattern but stick to it where possible.
    (`make_` and `process_` are terrible names which need to be renamed - perhaps `make_` and `run_`? [discuss here](https://github.com/nestauk/baking-cookies/issues/9))

-   Parameters should not be hard-coded but specified in `model_config.yaml`, loaded from the dictionary `baking_cookies.config`, and passed into the `make_` prefixed function.

    You could load the config in the `make_` function but consider whether this decreases transparency - less informative doc-strings for `make_` - or generalisability.

-   Don't use `print`, use the logging module, e.g. ``logger = logging.getLogger(__name__); logger.info('Logging at info level goes into `info.log`')``

# Training a model

We now have a cleaned dataset so now we wish to proceed with prototyping a model that predicts the lead Funder from the abstract texts.
The steps we need to follow are:

1.  Make an issue and new branch for model training
2.  Create a [new notebook](https://github.com/nestauk/baking-cookies/blob/gtr-projects/notebooks/dev/02_gr_gtr_funder_model.ipynb)
3.  Load cleaned data

   ![img](DS_workflow_tutorial_-__Nesta_Cookie_Cutter_Basic_ML_Tutorial/screenshot_2019-08-13_15-45-52.png)
4.  Train test split and save outputs (IDs)
5.  Create model pipeline (for training purposes)
   ![img](DS_workflow_tutorial_-__Nesta_Cookie_Cutter_Basic_ML_Tutorial/screenshot_2019-08-13_15-45-57.png)
6.  Fit and evaluate (at this point you might copy paste evaluation to lab book)
7.  Save model
   ![img](DS_workflow_tutorial_-__Nesta_Cookie_Cutter_Basic_ML_Tutorial/screenshot_2019-08-13_15-46-02.png)
8.  Add notebooks into WIP branch
9.  Factor out code and make a PR into `gtr-projects`

The model is very simple, it calculates TF-IDF features for each abstract and performs a logistic regression. 
Take a look through the [notebook](https://github.com/nestauk/baking-cookies/blob/gtr-projects/notebooks/dev/02_gr_gtr_funder_model.ipynb) to see the prototyping of the model, and compare this to the factored out code to understand where each of the constituent parts have gone.
We have split up the model pipeline into its constituent parts. This means that changes can be made to one part of the model pipeline (e.g. the train-test split strategy/size) without having to worry about searching through the full pipeline code. This also makes code easier to test. The constituent parts we have chosen are:

-   [Train-test split](https://github.com/nestauk/baking-cookies/blob/gtr-projects/baking_cookies/models/train_test_split.py)
-   [Training the model](https://github.com/nestauk/baking-cookies/blob/gtr-projects/baking_cookies/models/train_model.py)
-   [Evaluating the model](https://github.com/nestauk/baking-cookies/blob/gtr-projects/baking_cookies/models/evaluate.py)

Again we follow the `make_`, `process_` conventions; however in [`train_model.py`](https://github.com/nestauk/baking-cookies/blob/gtr-projects/baking_cookies/models/train_model.py) the model parameters are loaded in `make_train_model()`.

## **Exercise:**

Change this so that the config parameters are loaded in `__main__`, and add an option to pass in whether a `grid_search` is `True` or `False` from the command line using the `click` library (Hint: see [~make<sub>dataset.py</sub>](https://github.com/nestauk/baking-cookies/blob/dev/baking_cookies/data/make_dataset.py)).


<a id="orge80df29"></a>

# Data (and model) version control with DVC


<a id="org5406865"></a>

## What is DVC?

Data version control system for machine learning projects - makes data, models, and metrics shareable and reproducible.

![img](DS_workflow_tutorial_-__Nesta_Cookie_Cutter_Basic_ML_Tutorial/screenshot_2019-08-13_16-47-20.png)

-   Language agnostic
-   Integrates with Git
-   Storage: S3, Azure, GCP, SSH, etc.
-   Lightweight pipelines
-   Metric tracking
-   Open-Source and Self-Served : **Free**

**Use cases**

-   How do you avoid discrepancies between versions of source code and versions of data or models?
-   How do you keep track of which hyperparameter/feature changes contributed most to your target metric? And how do you recover old models without wasting time for the model to retrain?
-   How do you run a model's evaluation again without re-running everything?
-   How do you share models that take a long time to run (or maybe require a GPU) with colleagues who don't have time to wait / access to a GPU.


<a id="org5327fd3"></a>

## How does it work?

DVC tracks `<data or model filename>.dvc` meta-data files within your project's git repository which track the command and inputs necessary to compute a given output (e.g. dataset or model).
The actual data files are stored outside of the repository in a local cache (which can be pushed/fetched from remote data storage such as S3).

For example: The `model.pkl` file is a [file-link](http://www.tldp.org/LDP/intro-linux/html/sect_03_03.html) to a file in the local cache (in folder `.dvc/cache`) which corresponds to the MD5 hash stored in `model.pkl.dvc`.

If we change something in our DVC pipeline that results in `model.pkl` being different then `model.pkl.dvc` will reflect these changes in the MD5 hashes. We can then track the model version by tracking `model.pkl.dvc` in git (`git add model.pkl.dvc && git commit -m'New model' && git push`) and back-up the model (`dvc push`).

![img](DS_workflow_tutorial_-__Nesta_Cookie_Cutter_Basic_ML_Tutorial/screenshot_2019-08-13_16-49-27.png)

[See the docs](https://dvc.org/doc/understanding-dvc/how-it-works) for more.


<a id="orgb626dd1"></a>

## Putting `baking_cookies` under DVC

****NOTE****: This provides a high-level overview of how to specify a pipeline (DAG) in DVC (with git and S3 integration) such that the pipeline is shareable and reproducible; however more in-depth tutorials are available in the [extensive DVC documentation](https://dvc.org/doc).

To recap, thus far we've developed a pipeline that:

-   Fetches Gateway to Research project data
-   Processes it
-   Builds a train-test split
-   Trains a model on the abstract texts to predict who funded the work
-   Evaluates the classifier on the test set.

Now a colleague wants to try out the model and see if they can do better so we put the data and model under version control with DVC so we can track changes in these and easily share and receive models.

We write a script [`pipe/specify_dag.sh`](https://github.com/nestauk/baking-cookies/blob/7-dvc/pipe/specify_dag.sh) that specifies our pipeline commands as well as each stages dependencies and outputs and run the following to put the pipeline into DVC:

    $ dvc init
    $ cd pipe
    $ sh specify_dag.sh
    $ dvc remote add -d myremote s3://nesta-dvc-test/dvc~

Let's look at this process step by step:


### `dvc init`

This initialises a DVC project.

A new directory `.dvc/` will be created with `config` and `.gitignore` files and `cache` directory.
**These files and directories are hidden from the user generally and are not meant to be manipulated directly.**

`.dvc/cache` is one of the most important DVC directories. It will hold all the contents of tracked data files.
Note that `.dvc/.gitignore` lists this directory, which means that the cache directory is not under Git control. This is your local cache and you cannot push it to any Git remote.

We do want to put `.dvc/.gitignore` and `.dvc/config` under Git control, `dvc init` automatically runs `git add .dvc/.gitignore .dvc/config` (but not `git commit`).


<a id="org3dc9862"></a>

### `conda env export > ../conda_environment.yaml && git add ../conda_environment.yaml`

This command saves our conda environment so that the exact same package versions will be used.

This environment can be reproduced using `conda env create -f conda_environment.yaml`.


<a id="org6bee2c4"></a>

### Process GtR data

    $ dvc run -w ..\
        -d model_config.yaml\
        -d data/raw/gtr_projects.csv\
        -d data/aux/gtr_projects_abstractText_drop.txt\
        -d baking_cookies/data/gtr.py\
        -d baking_cookies/features/text_preprocessing.py\
        -o data/processed/gtr_tokenised.csv\
        python baking_cookies/data/gtr.py

    Running command:
            python baking_cookies/data/gtr.py
    ...
    <output from baking_cookies/data/gtr.py>
    ...
    Adding '../data/processed/gtr_tokenised.csv' to '../data/processed/.gitignore'.
    Saving '../data/processed/gtr_tokenised.csv' to '../.dvc/cache/27/67c6f0baf2a51b5a92f4957ea3dcf9'.
    Saving information to 'gtr_tokenised.csv.dvc'.
    
    To track the changes with git, run:
    
            git add ../data/processed/.gitignore gtr_tokenised.csv.dvc

We specify a stage of the pipeline using `dvc run ...`. The `-w ..` arguement tells us that the directory that commands are run from is one level up (recall we are in `pipe/`); `-d <filename>` specifies that this stage of the pipeline is dependent on the code/data in `<filename>`; `-o <filename>` specifies that this stage outputs `<filename>` and this should be tracked by DVC; and finally `python baking_cookies/data/gtr.py` is the command for this stage of the pipeline.

This stage of the pipeline reads and processes the data and depends on:

-   `model_config.yaml` - Our configuration parameters
-   `data/raw/gtr_projects.csv` - The raw input data
-   `data/aux/gtr_projects_abstractText_drop.txt` - Auxilliary data
-   `baking_cookies/data/gtr.py` - The script being run
-   `baking_cookies/features/text_preprocessing.py` - Local imports made by the script being run

This stage produces one output `data/processed/gtr_tokenised.csv` - our clean data.

    $ cat ../data/processed/.gitignore

    /gtr_tokenised.csv

The `.gitignore` file simply tells git not to concern itself with `gtr_tokenised.csv` as this is under the control of DVC (This isn't super important but means that you get much tidier `git status` summaries).

`$ git add ../data/processed/.gitignore gtr_tokenised.csv.dvc` - Finally, we put any `.gitignore` and `.dvc` files produced under git control as prompted by the output of `dvc run`.


<a id="org1889c9b"></a>

### Aside: what does a `.dvc` file look like?

    $ cat gtr_tokenised.csv.dvc

    md5: 19308d54c21c4da498b6ae1c75ac6126
    cmd: python baking_cookies/data/gtr.py
    wdir: ..
    deps:
    - md5: c25d832b9757fd567397ea729274eed9
      path: model_config.yaml
    - md5: f5c1443e275ad5701ac630af8eeb6ede
      path: data/raw/gtr_projects.csv
    - md5: 30657b88561c8e78088c0a725361acea
      path: data/aux/gtr_projects_abstractText_drop.txt
    - md5: 86b848be732b81aa5ef1cc8121e55256
      path: baking_cookies/data/gtr.py
    - md5: 3f6f7389173deba6c9567075a264d1c4
      path: baking_cookies/features/text_preprocessing.py
    outs:
    - md5: 2767c6f0baf2a51b5a92f4957ea3dcf9
      path: data/processed/gtr_tokenised.csv
      cache: true
      metric: false
      persist: false

`.dvc` files are a simple YAML format consist of a list. We can see that at the top-level `gtr_tokenised.csv.dvc` contains:

-   `md5`: md5 checksum for this stage
-   `cmd`: the command being run in this stage
-   `wdir`: the directory that `cmd` is run from
-   `deps`: a list of dependencies for this stage
-   `outs`: a list of outputs for this stage

A dependency entry consists of such fields:

-   `path`: path to the dependency, relative to the `wdir` path;
-   `md5`: md5 checksum for the dependency;

An output entry consists of such fields:

-   `path`: path to the output, relative to the `wdir` path;
-   `md5`: md5 checksum for the output;
-   `cache`: whether or not dvc should cache the output;
-   `metric`: whether or not this file is a metric file;

See [here](https://dvc.org/doc/user-guide/dvc-file-format) for more information on the `.dvc` file format.


### Test-train split

    $ dvc run -w ..\
      -d model_config.yaml\
      -d data/processed/gtr_tokenised.csv\
      -d baking_cookies/models/train_test_split.py\
      -o data/processed/gtr_leadFunder_id_train.csv\
      -o data/processed/gtr_leadFunder_id_test.csv\
      python baking_cookies/models/train_test_split.py

    Running command:
            python baking_cookies/models/train_test_split.py
    ...
    <output from baking_cookies/models/train_test_split.py>
    ...
    Adding '../data/processed/gtr_leadFunder_id_train.csv' to '../data/processed/.gitignore'.
    Adding '../data/processed/gtr_leadFunder_id_test.csv' to '../data/processed/.gitignore'.
    Saving '../data/processed/gtr_leadFunder_id_train.csv' to '../.dvc/cache/96/4f0bcccdad3c991a0b971867195082'.
    Saving '../data/processed/gtr_leadFunder_id_test.csv' to '../.dvc/cache/78/90e330ddfea691db6ef5cf5b016692'.
    Saving information to 'gtr_leadFunder_id_train.csv.dvc'.
    
    To track the changes with git, run:
    
            git add ../data/processed/.gitignore ../data/processed/.gitignore gtr_leadFunder_id_train.csv.dvc

As with the last stage of the pipeline we use `dvc run` to specify the working directory, dependencies, outputs, and command for this stage.

`$ git add ../data/processed/.gitignore gtr_leadFunder_id_train.csv.dvc` - once again we put any `.gitignore` and `.dvc` files produced under git control as prompted by the output of `dvc run`.


<a id="orgfb9954c"></a>

### Train-model

    $ dvc run -w ..\
        -d model_config.yaml\
        -d data/processed/gtr_tokenised.csv\
        -d data/processed/gtr_leadFunder_id_train.csv\
        -d baking_cookies/models/train_model.py\
        -o models/gtr_leadFunder.pkl\
        python baking_cookies/models/train_model.py

    Running command:
            python baking_cookies/models/train_model.py
    ...
    <output from baking_cookies/models/train_model.py>
    ...
    Adding '../models/gtr_leadFunder.pkl' to '../models/.gitignore'.
    Saving '../models/gtr_leadFunder.pkl' to '../.dvc/cache/7e/bb48ba3d17c3b486e01b81a9d4172d'.
    Saving information to 'gtr_leadFunder.pkl.dvc'.
    
    To track the changes with git, run:
    
            git add ../models/.gitignore gtr_leadFunder.pkl.dvc

Nothing new here, we use `dvc run` again.

`$ git add ../models/.gitignore gtr_leadFunder.pkl.dvc` - put any `.gitignore` and `.dvc` files produced under git control as prompted by the output of `dvc run`.

**NOTE:** Pickling does not result in reproducible hashes


<a id="orgf56c22a"></a>

### Evaluate model

    $ dvc run -w ..\
        -d model_config.yaml\
        -d data/processed/gtr_tokenised.csv\
        -d data/processed/gtr_leadFunder_id_test.csv\
        -d models/gtr_leadFunder.pkl\
        -d baking_cookies/models/evaluate.py\
        -o reports/figures/gtr_leadFunder_confusion_matrix.png\
        -M models/metrics.json\
        -f Dvcfile\
        python baking_cookies/models/evaluate.py

    Running command:
            python baking_cookies/models/evaluate.py
    ...
    <output from baking_cookies/models/evaluate.py>
    ...
    Adding '../reports/figures/gtr_leadFunder_confusion_matrix.png' to '../reports/figures/.gitignore'.
    Output '../models/metrics.json' doesn't use cache. Skipping saving.
    Saving '../reports/figures/gtr_leadFunder_confusion_matrix.png' to '../.dvc/cache/56/f9cc780386215cb6a8790f8505ee2a'.
    Saving information to 'Dvcfile'.
    
    To track the changes with git, run:
    
            git add ../reports/figures/.gitignore Dvcfile

For the last stage of the pipeline something slightly different happens - we have extra `-M` and `-f` arguements.

`-M` denotes a metric file - usually a small human readable file (JSON, CSV, etc.) with some numbers or other information that describes a model or other outputs. In our case it is a JSON file containing precision, recall, f1-score and support for each class in our classifier.

`-f` simply specifies the name of the DVC file which is generated - by default the DVC file name generated is `<file>.dvc` where `<file>` is the file name of the first output (e.g. `-o` or `-M`) as we have seen before. Giving this the special name `Dvcfile` means that running the `dvc repro` command without arguements will run this file (and thus our whole pipeline).

`$ git add Dvcfile ../models/metrics.json ../reports/figures/.gitignore`


<a id="orgb1156b1"></a>

### `dvc remote add -d myremote s3://nesta-dvc-test/dvc`

Like in Git we add a remote (e.g. a Github URL) to push our code to, here we add an S3 bucket as a remote for DVC allowing us to push/pull tracked data and models relating to different git commits to/from an s3 bucket.

    $ cat .dvc/config

    ['remote "myremote"']
    url = s3://nesta-dvc-test/dvc
    [core]
    remote = myremote


<a id="orgf35db34"></a>

### `dvc push -r myremote`

Lets push our local cache to S3.

    $ dvc push -r myremote

    Preparing to upload data to 's3://nesta-dvc-test'/dvc
    Preparing to collect status from s3://nesta-dvc-test/dvc
    Collecting information from local cache...
    [##############################] 100%
    
    Collecting information from remote cache...
    [##############################] 100%
    [##############################] 100% Analysing status
    [##############################] 100% ../reports/figures/gtr_leadFunder_confusion_matrix.png
    [##############################] 100% ../data/processed/gtr_leadFunder_id_test.csv
    [##############################] 100% ../data/processed/gtr_leadFunder_id_train.csv
    [##############################] 100% ../models/gtr_leadFunder.pkl
    [##############################] 100% ../data/processed/gtr_tokenised.csv


<a id="org3a1a3c3"></a>

## Share the model

    git clone https://github.com/nestauk/baking-cookies
    cd baking-cookies
    git checkout dvc-tutorial-share-1
    conda env create -f conda_environment.yaml -n baking-cookies --force
    pip install -e .  # install repo as package 
    conda activate baking-cookies
    make sync_data_from_s3  # get data/raw
    dvc pull -r myremote  # equivalent: dvc fetch && dvc checkout
    cd pipe
    dvc repro


<a id="org409580c"></a>

## Make changes to the model

We want to now try and make improvements to the models by using Word2Vec to train embeddings and use these as features in a model.

`git checkout -b new-model-feature`

We create `baking-cookies/features/build_features.py` and `baking-cookies/features/w2v.py` which build the word embeddings - this involves a new step in our pipeline so we have to specify it using `dvc run`:

    $ dvc run -w .. \
        -d model_config.yaml\
        -d data/processed/gtr_tokenised.csv\
        -d baking-cookies/features/w2v.py\
        -d baking-cookies/features/build_features.py\
        -o models/gtr_w2v\
        -o data/processed/gtr_embedding.csv\
        python baking-cookies/features/build_features.py

`git add ../models/.gitignore ../data/processed/.gitignore gtr_w2v.dvc`

We must also modify the train-test split and model training steps to reflect these updated features:


<a id="orgf741b86"></a>

### EXERCISE

-   Checkout \`18-w2v-exercise\` branch
-   Update the `pipe/specify_dag.sh` file to reflect the updates to the pipeline
-   Run the file to update the pipelines
-   `dvc_repro`


<a id="org8e01247"></a>

## Revisit an old model <span style="color:red">[Incomplete]</span>

- `git checkout 7-dvc`
- `dvc pull`
- `dvc repro`

No need to run any expensive computations.

# Publishable notebooks <span style="color:red">[Incomplete]</span>

- Share interim analyses as Gists
- Save final notebooks as html files and put in `reports/`. These are for presenting results and thus should:
  - Document the purpose of the notebook at the top
  - Provide discussion throughout the document
  - Import and run functions - *not* define them
  - Ideally be readable and understandable with the code hidden (unless you are demonstrating code usage of course)


# Testing <span style="color:red">[Incomplete]</span>

# Tools/tips <span style="color:red">[Incomplete]</span>

## nbextensions + configurator

### Gist-it
### Autopep8
### Hide input
### Select CodeMirror Keymap
### ExecuteTime

## Magics
[Full list here](https://ipython.readthedocs.io/en/stable/interactive/magics.html)

### `%debug`
### `%pdb`
### `%env` / `%set_env`
### `%run`
### `%psearch`
### `%autoreload`
## Profilers

1.  `%prun`
2. `mprof` - https://pypi.org/project/memory-profiler/
