# Docs for contributors

## Github actions

There are several workflows in `.github/workflows`:

- `docs.yml` - Deploys documentation to github pages on push to master (e.g. after PR merged)
- `release.yml` - Drafts release notes based on merged PR's
- `labeler.yml` - Sets the repository to use the issue labels defined in `.github/labels.yml`
- `test.yml` - Runs tests on PR's or on push to master (e.g. after PR merged)

## Release process

- Each PR should have a `major`/`minor`/`patch` label assigned based on the desired version increment, e.g. `minor` will go from `x.y.z -> x.(y+1).z`
- After a PR is merged then draft release notes will be generated/updated [here](https://github.com/nestauk/ds-cookiecutter/releases) (see `release.yml` above)
- In the Github UI: rewrite the drafts into something informative to a user and then click release
  - :warning: Releases should be made little and often - commits on `master` are immediately visible to cookiecutter users

## Documentation

Lives under `docs/`, see [`docs/README.md`](docs/README.md).
