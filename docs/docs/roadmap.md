# Roadmap

## Metaflow

In the coming weeks we will be rolling out utilities to make working with metaflow easier.

For example, you will be able to specify the following YAML file and then run a command like `nestaflow sic_classifier` and the corresponding metaflow pipeline will run on AWS batch with 8 CPU's, 64GB RAM with the configuration parameters specified in `flow_kwargs`.

```yaml
#file: src/config/pipeline/sic_classifier.yaml
preflow_kwargs:
    with: batch,cpu=8,memory=64000
flow_kwargs:
    documents_path: inputs/data/descriptions.json
    freeze-model: false
    config:
        encode:
            add_special_tokens: true
            max_length: 64
            pad_to_max_length: true
```

Furthermore, successful runs will be tracked in version control allow data getters you write for metaflows to automatically fetch the right flow results.

## `ds-utils`

Development of [`ds-utils`](https://github.com/nestauk/ds-utils/) will begin soon.

This will be a package providing well tested and documented data science utilities based on our previous data-science projects.

## Reporting

In a few recent projects we have been experimenting with a report workflow using [pandoc](https://pandoc.org/) to generate HTML and PDF (LaTeX) outputs from a single ([pandoc flavoured](https://pandoc.org/MANUAL.html#pandocs-markdown)) markdown file, including facilitating the trivial inclusion of interactive [altair](https://altair-viz.github.io/index.html) plots within HTML outputs.

After further refinement of this workflow and development of a simple report generation tool, this can be incorporated into the cookiecutter.

## flake8

-   Identification of a suitable starting `flake8` configuration and a plan to phase in the number of cases handled by `flake8` (to avoid an overwhelming start).
-   Incorporation of `flake8` into the pre-commit hooks.

Note: you can already lint your code using (a quite opinionated) flake8 configuration defined in `setup.cfg` by running `make lint`.

## Poetry

Investigate a switch to managing dependencies and packaging with [poetry](https://python-poetry.org/) (falling back on Conda only when necessary).

This will provide much more robust dependency management and a simplification of the packaging utilities.

This tool is not being integrated into the overhauled cookiecutter from day one to avoid user overwhelm.

## Docker

Investigate the utility of automatically containerisation data-science project.

## Schema

Investigate the use of [pydantic](https://pydantic-docs.helpmanual.io/) to document data-schemas and provide data-validation where required.

This has the benefit of ensuring documentation stays up to date, and provides the ability to generate schemas in alternative forms such as [converting to SQLalchemy](https://github.com/tiangolo/pydantic-sqlalchemy) and outputting in language-agnostic formats such as [JSON schema](https://pydantic-docs.helpmanual.io/usage/schema/).

## CI/CD

Use Github actions to: - Automatically build a Docker container of the project - Automatically run tests - Perform `pre-commit` actions on the server to guard against user error

## Configuration

Investigate options for Machine-learning oriented configuration management - e.g. with [gin](https://github.com/google/gin-config) or the approach used by [thinc](https://thinc.ai/docs/api-config).
