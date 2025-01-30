#!/bin/bash

# Remove environment.yaml if not using conda
# Set path, trim whitespace, and then remove if it exists
path='{% if cookiecutter.venv_type != "conda" %} environment.yaml {% endif %}'
path=$(echo "$path" | xargs)
if [ -n "$path" ] && [ -e "$path" ]; then
    rm "$path"
fi

# Permit auto-loading of .envrc
direnv allow

# Create git repo
git init -q

# Setup empty main and dev
git checkout -b main -q
git add .
git commit -am "Setup Nesta Data Science cookiecutter" -q
git checkout -b dev -q

# Create remote repository 
REPO_NAME="{{ cookiecutter.project_slug }}"
OPENNESS="{% if cookiecutter.openness == 'private' %}--private{% else %}--public{% endif %}"
gh repo create "$REPO_NAME" $OPENNESS --source=. --remote=origin --push

# Transfer the repository to the organisation
gh repo transfer "nesta-cookiecutter-test/$REPO_NAME" --confirm

# Create issue on github_support

ISSUE_TITLE="Configure repository: $REPO_NAME"
ISSUE_BODY="Repository setup requested for $REPO_NAME

Please configure:
- Branch protection rules
- Team access
- Any other standard Nesta repository settings

Thank you!"

gh issue create --repo nestauk/github_support --title "$ISSUE_TITLE" --body "$ISSUE_BODY"

ISSUE_NUMBER=$(gh issue create --repo nestauk/github_support --title "$ISSUE_TITLE" --body "$ISSUE_BODY" --json number -q .number)

echo "Repository created and transferred: https://github.com/nesta-cookiecutter-test/$REPO_NAME"
echo "Support issue created: https://github.com/nesta-cookiecutter-test/github_support/issues/$ISSUE_NUMBER"
echo "Configured git repo at $(pwd), please enter the project directory & run 'make install'"
