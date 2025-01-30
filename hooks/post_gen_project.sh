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
GITHUB_USER=$(gh api user | jq -r '.login')
REPO_NAME="{{ cookiecutter.repo_name }}"
OPENNESS="{% if cookiecutter.openness == 'private' %}--private{% else %}--public{% endif %}"
gh repo create $REPO_NAME $OPENNESS --source=. --remote=origin --push

# Transfer the repository to the organisation
gh api "repos/$GITHUB_USER/$REPO_NAME/transfer" -f "new_owner=nesta-cookiecutter-test"

# Create issue on github_support

ISSUE_TITLE="Configure repository: $REPO_NAME"
ISSUE_BODY="Repository setup requested for $REPO_NAME

Please configure:
- Branch protection rules
- Team access
- Any other standard Nesta repository settings

Thank you!"

ISSUE_URL=$(gh issue create --repo nesta-cookiecutter-test/github_support --title "$ISSUE_TITLE" --body "$ISSUE_BODY")

echo "Repository created and transferred: https://github.com/nesta-cookiecutter-test/$REPO_NAME"
echo "Support issue created: $ISSUE_URL"
echo "Configured git repo at $(pwd), please enter the project directory & run 'make install'"
