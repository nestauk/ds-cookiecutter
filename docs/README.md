## Generating the docs

Install requirements:

    pip install -r requirements.txt

Change directories into the docs folder:

    cd docs

Use [mkdocs](http://www.mkdocs.org/) structure to update the documentation. Test locally with:

    mkdocs serve

Docs are automatically published to `gh-pages` branch via. Github actions after a PR is merged into `master`.