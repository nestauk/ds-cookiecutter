# Features

## Config driven parameterisation

```yaml
preflow_kwargs:
  datastore: s3
  metadata: local
  with: "batch:cpu=1"
  environment: conda
  package-suffixes: ".py,.txt,.md,.yaml"
flow_kwargs:
  info:
    ds_type:  # value of `ds_type` is the result of `random.betavariate(1, beta=10)` hook:  
        name: "random.betavariate"
        args:
          [1]
        kwargs:
          beta: 10
```

## Bundling - use full package

## Getter caching

## Version control of Run ID's

# TODO

- usernames + tags
  - tag with project name
  - project namespace?
  - clear data for a user on this project
- CLI tool polish
- Cache getters

# Issues

- Need the default to be `package-suffixes: ".py,.txt,.md,.yaml"` if `son_of_batch` is used