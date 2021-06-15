# Coupling to ds-cookiecutter

Currently, `flowrider` is coupled to `ds-cookiecutter` in the following places:

- `flowrider.py`: Typer CLI level with `flowrider/`
  1. Assumes the calling package is alongside `flowrider/` on the filesystem
  2. Assumes config in: `{PKG_NAME}/config/pipeline/{FLOW_SUBPATH}_{TAG}.yaml`
  3. Assumes flow in: `{PKG_NAME}/pipeline/{FLOW_SUBPATH}.py`

# Metaflow Gotchas and pain-points

- Painful CLI experience - Passing many options is cumbersome
  - **Solution:** YAML-based config + CLI wrapper
- No mechanism for "runtime injection"
  - **Solution:** Config "hooks"
- Metaflow only packages file/folders at or below the flow in the file hierarchy meaning project-level utilities cannot be shared in separate conda/batch environments
  - **Solution:**
    - CLI wrapper temporarily copies (and executes) flow to project base directory
    - `flowrider.decorators.son_of_a_batch` install project requirements
- Can't install pip-only dependencies for a flow/step
  - **Solution:** `flowrider.decorators.pip`

# Features

## CLI

### Config driven parameterisation

```yaml
preflow_kwargs:
  datastore: s3
  metadata: local
  with: "batch:cpu=1"
  environment: conda
  package-suffixes: ".py,.txt,.md,.yaml"
flow_kwargs:
  random_seed:
tags: ["my extra tag", "another one"]
```

#### Hooks

```yaml
preflow_kwargs:
  datastore: s3
  metadata: local
  with: "batch:cpu=1"
  environment: conda
  package-suffixes: ".py,.txt,.md,.yaml"
flow_kwargs:
  deployment_info:
    hook:
      # Imports and calls this function substituting the result as the value of `deployment_info`
      name: project_name.pipeline.example.example_flow.hook
      args: 1
      kwargs:
        b: 2
```

### Bundling - use full package

- Copies project to a temporary directory
- Copies flow file to base of project directory s.t. can bootstrap extra ops with `flowrider.decorators.*`
  - E.g. decorating Flow class with `flowrider.decorators.son_of_a_batch` to install package requirements from `requirements.txt`

### Version control of Run ID's

Writes successfull runs alongside corresponding YAML with same filename but `.run_id` suffix.

E.g. if YAML config is in `config/pipeline/example/example_flow_local.yaml` then `config/pipeline/example/example_flow_local.run_id` contains the last successful run ID corresponding to the running of that YAML config.

### Organising results

Adds tag based on `REPO_NAME` of project

## Decorators

### `flowrider.decorators.son_of_a_batch`

Installs your cookiecutter "package" (and its `requirements.txt`) in whatever environment the flow is running in.

### `flowrider.decorators.pip`

Works like `metaflow.conda` decorator but for pip.

WARNING: If not running in a separate environment, e.g. using `environment: conda` in `preflow-kwargs` then this may overwrite dependencies.

## `flowrider.client.getter.auto_getter`

```python
from flowrider.metaflow_client import auto_getter
from project_name.pipeline.example.example_flow import EnvironmentFlow
import project_name

artifact = "info"
config_path = "config/pipeline/example/example_flow_local.yaml"
MODULE = project_name

auto_getter(EnvironmentFlow, config_path, artifact, MODULE, cache_strategy=None)  # No caching
auto_getter(EnvironmentFlow, config_path, artifact, MODULE)  # Cached by default with `flowrider.cache.cache_getter_fn`
```

Getters are cached (via. pickle) based on:

- flow name
- run ID
- artifact

By default in your systems temporary directory, e.g. `/tmp/`, but can be overwritten setting `FLOWRIDER_TEMP_DIR` environment variable (we recommend `outputs/.cache/`)

# TODO

- CLI tool polish

  - Docs
  - Resume functionality?
  - Pass through other commands to metaflow? `--` syntax?
    - E.g. `flowrider example/example_flow -- show` runs `python .../pipeline/example/example_flow.py show`

- `flowrider.client.getter.auto_getter` untested for Flows outside the project! (e.g. `ds-utils`)
