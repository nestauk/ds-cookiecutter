#!/bin/bash
set -euo pipefail

ORG="nestauk"
REPO_NAME="{{ cookiecutter.repo_name }}"
VISIBILITY="{% if cookiecutter.openness == 'private' %}--private{% else %}--public{% endif %}"

# Remove environment.yaml if not using conda
path='{% if cookiecutter.venv_type != "conda" %} environment.yaml {% endif %}'
path=$(echo "$path" | xargs)
if [ -n "$path" ] && [ -e "$path" ]; then
    rm "$path"
fi

# Permit auto-loading of .envrc
direnv allow

# Local git setup
git init -q
git checkout -b main -q
git add .
git commit -am "Setup Nesta Data Science cookiecutter" -q
git checkout -b dev -q

{% if cookiecutter.create_remote == 'yes' %}
# Verify gh auth before touching remote
if ! gh auth status >/dev/null 2>&1; then
    echo "Error: gh not authenticated. Run 'gh auth login' then push manually." >&2
    exit 1
fi

# Create remote in nestauk org, push both branches, default to dev
gh repo create "$ORG/$REPO_NAME" $VISIBILITY --source=. --remote=origin
git push -u origin main
git push -u origin dev
gh repo edit "$ORG/$REPO_NAME" --default-branch dev

echo "Repo: https://github.com/$ORG/$REPO_NAME"
{% endif %}
echo "Configured git repo at $(pwd), enter project directory & run 'make install'"
