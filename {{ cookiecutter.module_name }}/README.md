# {{cookiecutter.project_name}}

## Setup

{% if cookiecutter.venv_type == 'uv' -%}
This project uses [`uv`](https://docs.astral.sh/uv/) for virtual environment management. If you are new to `uv`, you can find the [quickstart guide here](https://docs.astral.sh/uv/getting-started/).
{%- elif cookiecutter.venv_type == 'venv' -%}
This project uses Python's built-in [`venv`](https://docs.python.org/3/library/venv.html) for virtual environment management. If you are new to `venv`, you can find the [quickstart guide here](https://docs.python.org/3/library/venv.html#creating-virtual-environments).
{%- elif cookiecutter.venv_type == 'conda' -%}
This project uses [`conda`](https://docs.conda.io/en/latest/) for virtual environment management. If you are new to `conda`, you can find the [quickstart guide here](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html).
{%- endif %}

We also utilise `direnv` via the `.envrc` file to automatically:

- Import your environment variables from `.env`
- Activate your virtual environment (_only if you comment out the relevant lines in `.envrc`_)

After installing `direnv`{% if cookiecutter.venv_type == 'uv' or cookiecutter.venv_type == 'conda' %} and {% endif %}{% if cookiecutter.venv_type == 'uv' -%}`uv`{%- elif cookiecutter.venv_type == 'conda' -%}`conda`{%- endif %} on your system (we recommend doing this via [`brew`](https://brew.sh/) on macOS), you **must** run the following commands in your terminal to set up the project:

```bash
direnv allow
{% if cookiecutter.venv_type == 'uv' -%}
uv sync
uv run pre-commit install --install-hooks
{%- elif cookiecutter.venv_type == 'venv' -%}
python -m venv .venv
source .venv/bin/activate
pip install ".[dev]"
pre-commit install --install-hooks
{%- elif cookiecutter.venv_type == 'conda' -%}
conda env create -f environment.yaml
conda activate {{ cookiecutter.module_name }}
pip install ".[dev]"
pre-commit install --install-hooks
{%- endif %}
```

{% if cookiecutter.use_r == 'yes' %}### R Setup

_Note: even if you plan to only work in R, you still **must** set up the Python environment as described above for pre-commit hooks and other potential Python dependencies._

This project uses [`renv`](https://rstudio.github.io/renv/) for R package management. If you are new to `renv`, you can find the [quickstart guide here](https://rstudio.github.io/renv/articles/renv.html).

To set up `renv` and the R environment in this repo, run the following commands in your terminal:

```bash
Rscript -e "if (!requireNamespace('renv', quietly = TRUE)) install.packages('renv', repos='https://cloud.r-project.org')"
Rscript -e "renv::install()"
```

As you add new R packages to your project, you can run `renv::snapshot()` to update the `renv.lock` file and commit the changes to `git`, which will ensure that others can recreate the same environment.

For working with AWS services, you will need to set up an `.Renviron` file at the root of your project specifying the region to use, for most projects this file should be:

```
AWS_DEFAULT_REGION=eu-west-2
AWS_REGION=eu-west-2
```

If you use RStudio, we recommend opening this folder via "Open Project" and committing the `.Rproj` file to your repository, as it contains useful project settings for ensuring reproducibility when others work on the project.

{% endif %}## Contributor guidelines

[Technical and working style guidelines](https://github.com/nestauk/ds-cookiecutter/blob/master/GUIDELINES.md)

### Versioning

We use [Semantic Versioning](https://semver.org/) for versioning. This project's versioning is inferred dynamically at build via `hatchling`, based on the value in the base `__init__.py` file.

To update and release the package:

1. Update the version in `{{ cookiecutter.module_name }}/__init__.py` (and any other relevant places)
2. Open a release PR with the version changes
3. Once approved and merged, create a new release and tag on GitHub with the matching version number
4. User's can then install the package via `uv add <repository URL> --tag <version>`

---

<small><p>Project based on <a target="_blank" href="https://github.com/nestauk/ds-cookiecutter">Nesta's data science project template</a>
(<a href="http://nestauk.github.io/ds-cookiecutter">Read the docs here</a>).
</small>
