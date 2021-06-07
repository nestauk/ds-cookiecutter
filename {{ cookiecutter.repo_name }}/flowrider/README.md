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
```

#### Hooks

```yaml
preflow_kwargs:
  datastore: s3
  metadata: local
  with: "batch:cpu=1"
  environment: conda
  package-suffixes: ".py,.txt,.md,.yaml"
flow_kwargs: {}
```

### Bundling - use full package

- Copies project to a temporary directory
- Copies flow file to base of project temporary directory s.t. local package can all be imported and used in flow.
  - Requires decorating Flow class with `flowrider.decorators.son_of_a_batch` to install package requirements from `requirements.txt`

### Version control of Run ID's

Writes successfull runs to `config/pipeline/{FLOW_SUBPATH}_{TAG}.run_id`

## Decorators

### `flowrider.decorators.son_of_a_batch`

Installs your cookiecutter "package" (and its `requirements.txt`) in whatever environment the flow is running in.

### `flowrider.decorators.pip`

Works like `metaflow.conda` decorator but for pip.

WARNING: If not running in a separate environment, e.g. using `environment: conda` in `preflow-kwargs` then this may overwrite dependencies.

## `flowrider.client.getter.auto_getter`

```python
from flowrider.metaflow_client import auto_getter


path, tag, artifact = "foo", "dev", "info"
auto_getter(path, tag, artifact, cache_strategy=None)  # No caching
auto_getter(path, tag, artifact)  # Cached by default with `flowrider.cache.cache_getter_fn`
```

Getters are cached (via. pickle) based on:
- flow name
- run ID
- artifact

By default in `outputs/.cache/` but can be overwritten setting `FLOWRIDER_TEMP_DIR` environment variable
# TODO

- usernames + tags
  - tag with project name
  - project namespace?
  - clear data for a user on this project
- CLI tool polish
- Cache getters
