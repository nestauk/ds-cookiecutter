## Generating the docs

Install requirements:

    pip install -r requirements.txt

Change directories into the docs folder:

    cd docs

Use [mkdocs](http://www.mkdocs.org/) and [mkdocs material](https://squidfunk.github.io/mkdocs-material/) structure to update the documentation. Test locally with:

    mkdocs serve

:note: mkdocs material uses a superset of Markdown, see [the reference](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)

Docs are automatically published to `gh-pages` branch via. Github actions after a PR is merged into `master`.

