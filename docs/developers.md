# Developers guide

## Usage

### Installation

This project uses [`uv`](https://docs.astral.sh/uv/) to manage the virtual environment. To install the project, run:

```bash
uv sync
uv run pre-commit install --install-hooks
```

This will create a virtual environment in `.venv` and install the dependencies listed in `pyproject.toml`.

You can then go on to build docs, run tests, etc. using `uv run` commands.

### Documentation

We use [mkdocs](http://www.mkdocs.org/) and [mkdocs material](https://squidfunk.github.io/mkdocs-material/) to maintain documentation. You can test them locally with:

```bash
uv run mkdocs serve
```

:note: mkdocs material uses a superset of Markdown, see [the reference](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)

Docs are automatically published to `gh-pages` branch via. Github actions after a PR is merged into `master`.

### Testing

We use [pytest](https://docs.pytest.org/en/latest/) to run tests. You can run them with:

```bash
uv run pytest
```

You can also run tests with coverage using:

```bash
uv run pytest --cov=.
```

## Github actions

There are several workflows in `.github/workflows`:

-   `docs.yml` - Deploys documentation to github pages on push to master (e.g. after PR merged)
-   `release.yml` - Drafts release notes based on merged PR's
-   `labeler.yml` - Sets the repository to use the issue labels defined in `.github/labels.yml`
-   `test.yml` - Runs tests on PR's or on push to master (e.g. after PR merged)

## Release process

-   Each PR should have a `major`/`minor`/`patch` label assigned based on the desired version increment, e.g. `minor` will go from `x.y.z -> x.(y+1).z`
-   After a PR is merged then draft release notes will be generated/updated [here](https://github.com/nestauk/ds-cookiecutter/releases) (see `release.yml` above)
-   In the Github UI: rewrite the drafts into something informative to a user and then click release
    -   :warning: Releases should be made little and often - commits on `master` are immediately visible to cookiecutter users
