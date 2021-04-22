# FAQ

## How do I update the conda environment (`environment.yaml`)?

As you install extra libraries add them to `environment.yaml`.

If you're not sure what libraries you have installed you can use `conda env export` to print out all the versions of your current environment; however this will list indirect dependencies too so don't blindly add everything!

Try to be specific about what version of a library is required, but not to specific.
For example, `pandas=0.25,<1.0` or `pandas=0.25.3` **NOT** `pandas=0.25.3=py36hb3f55d8_0`.
Being specific decreases the likelihood of a new release breaking your code or a collaborator having an incompatible version. Being too specific means it's likely no-one can reproduce your environment.

## Where should I save models?

Save trained models in `output/models/`.

## Where do I save figures?

`outputs/figures`

## What do my notebooks go?

Identify where the functionality should be, and add a `notebooks/` folder there to prototype within.

## How should I use `config/model_config.yaml`

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

TODO: UPDATE

## Docstrings

Any exposed function or class should have a google style docstring.

Functions for internal use only should have a leading underscore (e.g. `_my_fun`), and do not require full docstrings.

See https://www.sphinx-doc.org/en/1.7/ext/example_google.html for examples of how to format docstrings.

Flake8 will warn you about missing docstrings and incorrectly formatted docstrings.

## Sharing notebooks

We use [jupytext](jupytext.io) to pair `.ipynb` files with a human-readable and git-diffable `.py` file.
These paired `.py` files should be committed to git, `.ipynb` files are git-ignored.

If you need to share the visual content of a notebook, either exported as HTML or as a gist using [gist-it](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/gist_it/readme.html).
