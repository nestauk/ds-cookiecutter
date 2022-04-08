# FAQ

Please submit questions as a [Github issue](https://github.com/nestauk/ds-cookiecutter/issues/new) with the label "question".

## What customisations can I make when setting up the cookiecutter?

You should give thought when modifying the cookiecutter - big breaking changes defeat the point of having a standard starting point.

The other side of the equation is having a hackable standard starting point - the cookiecutter aims to be small and simple enough to understand which allows customisation based on needs that can't be centrally anticipated.

The `.recipes/` folder provides scripts/docs for extending the cookiecutter with specific bits of functionality we think are important but are either:

-   Not suitable in every situation
-   Not generically configurable for every situation
-   Too much complex to be a cookiecutter default

This keeps the core of the cookiecutter lean, maintainable, and hackable.

!!! info "Older versions of the cookiecutter were more opinionated"

    However trying to meet all needs means the cookiecutter ends up too complex and too brittle leaving little room/incentive for sub-teams/projects to understand and extend the cookiecutter to better solve their problems which results in a sub-optimal solution for everyone.

## Where should I save models?

-   If it's a pre-trained model someone has sent you: `inputs/models/`
-   If it's a model you have trained: `outputs/models/`
