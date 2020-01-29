# FAQ

## How do I update `conda_environment.yaml`?

As you install extra libraries add them to `conda_environment.yaml`.

If you're not sure what libraries you have installed you can use `conda env export` to print out all the versions of your current environment; however this will list dependencies too so don't blindly add everything!

If you require specific versions of libraries, try to make these as general as possible to increase the probabiliity of somebody using a different machine being able to reproduce your environment.
For example, `pandas >0.25,<0.26` not `pandas=0.25.3=py36hb3f55d8_0`.

## I didn't configure an s3 bucket at start-up, how do I do it?

Open `Makefile` and edit the right-hand side of `BUCKET = ...` line so that is the name of your s3 bucket (don't include `s3://`).

## How should I put data into `data/raw`

Edit `fetch_data.py` in the source folder to fetch any data from the web (from S3/SQL/an API etc.).

Running `make fetch` will run this then sync the `data/raw` folder to s3

## Where should I save models?

Save trained models in `models/` as something like a pickle (`.pkl`) file.

## Where do I get data?

Use `make sync_data_from_s3` to get the data from `data/raw` (as long as whoever set up the repo has configured an s3 bucket and used `make sync_data_to_s3`).


## How do I format code?

Running `make lint` will format code in the directory named after your repo using [`black`](https://black.readthedocs.io/).
> Black makes code review faster by producing the smallest diffs possible. Blackened code looks the same regardless of the project you’re reading. Formatting becomes transparent after a while and you can focus on the content instead.

## Where do I save figures?

`reports/figures`

## Where should I put "X" functionality?

Common sense applies but generally:

- If it's specific to a dataset, create a subfolder based on the dataset
- It it's a generic estimator (does `transform` but not `fit`) put it in `estimators/`.
  - Pre-trained models fetched from e.g. tensorflow hub, should go here too
- If it's a generic transfomers (does `fit`) put it in `transformers/`
- If it creates a visualisation, put it in `visualisation/`

## What is a `dev` notebook?
`dev` notebooks are for exploration and experimention. 

A guiding principle: If someone else has to look inside your `dev` notebook, something has gone wrong (see "What shouldn't be in a notebook?")

## What shouldn't be in a notebook?

Notebooks should serve two purposes:

1) Exploration/experimentation: `notebooks/dev`
2) Presention: `notebooks/`

If you have a notebook containing code that creates an asset (fetches data/processes data/defines a model/trains a model/produces a final plot etc. ), this should be refactored into a `.py` file in the source directory (see "Where should I put "X" functionality?").

## How should I use `model_config.yaml`

Configurable hyper-parameters should go in here.

There should be no magic numbers in function bodies.

If you're sure a number will not change (maybe it represents a fixed API ratelimit), define it in the main body of the file with an all-caps name to signal it's constant nature (e.g. `MAX_REQUESTS_PER_SEC = 30`).

If it's a hyper-parameter (e.g. the number of trees in a random forest, or a random seed), put it in `model_config.yaml`:

```yaml
gtr_data:
  random_forest:
    seed: 0
    n_estimators: 100
```

Fetch the value in the relevant file like so:
```python

import <repo_name>

...

seed = <repo_name>.config['gtr_data']['random_forest']['seed']
```

Depending on the repo size, different levels of nesting in the config may be appropriate (E.g. If you only have one model and one dataset, no nesting is fine)

## Docstrings

Any exposed function or class should have a google style docstring.

Functions for internal use only should have a leading underscore (e.g. `_my_fun`), and do not require full docstrings.

See https://www.sphinx-doc.org/en/1.7/ext/example_google.html for examples of how to format docstrings.

## Sharing notebooks

The cookiecutter installs a git hook to strip notebooks of output before commiting. This gives cleaner diff's, and stops repo bloat.

If you `git clone` a cookiecutter repo and plan on making commits you should run `make git` to install this git hook.

Notebooks should be shared with collaborators outside of the main git repository, either exported as HTML or as a gist using something like [gist-it](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/gist_it/readme.html).


