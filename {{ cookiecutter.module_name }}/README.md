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

## Contributor guidelines

[Technical and working style guidelines](https://github.com/nestauk/ds-cookiecutter/blob/master/GUIDELINES.md)

---

<small><p>Project based on <a target="_blank" href="https://github.com/nestauk/ds-cookiecutter">Nesta's data science project template</a>
(<a href="http://nestauk.github.io/ds-cookiecutter">Read the docs here</a>).
</small>
