# FAQ

Please submit questions as a [Github issue](https://github.com/nestauk/ds-cookiecutter/issues/new) with the label "question".

## What customisations can I make when setting up the cookiecutter?

You should be careful about modifying the cookiecutter - big changes defeat the point of having a standard project template.

The other side of the equation is having a hackable standard starting point - the cookiecutter aims to be small and simple enough to understand which allows customisation based on needs that can't be centrally anticipated (but we encourage those customisations to be fed back to us as an issue).

Some things that might be reasonable:
- Remove initial dependencies you know you won't need
- Add dependencies you know you'll need
- Extra documentation
- Add subfolder structure right away to help co-ordinate work
- Replace conda with a different virtual environment / dependency management tool


## Where should I save models?

- If it's a pre-trained model someone has sent you: `inputs/models/`
- If it's a model you have trained: `outputs/models/`
