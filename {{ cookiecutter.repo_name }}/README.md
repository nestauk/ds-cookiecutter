{{cookiecutter.project_name}}
==============================

{{cookiecutter.description}}

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make dvc`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── README.md
    │   ├── external       <- Data from third party sources.
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
    │   ├── notebook_preamble.ipy
    │   │                     
    │   └── dev            <- Development notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `_` delimited description, e.g.
    │                         `01_jmg_eda.ipynb`.
    │
    ├── pipe               <- Contains DVC pipeline files
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so {{ cookiecutter.repo_name }} can be imported
    │
    ├── {{ cookiecutter.repo_name }}                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes {{ cookiecutter.repo_name }} a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


--------

<p><small>Project based on the <a target="_blank" href="https://github.com/nestauk/cookiecutter-data-science-nesta">Nesta cookiecutter data science project template</a>.</small></p>
