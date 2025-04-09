#!/bin/bash

# Remove environment.yaml if not using conda
# Set path, trim whitespace, and then remove if it exists
path='{% if cookiecutter.venv_type != "conda" %} environment.yaml {% endif %}'
path=$(echo "$path" | xargs)
if [ -n "$path" ] && [ -e "$path" ]; then
    rm "$path"
fi

# Create git repo
git init -q

# Setup empty main and dev
git checkout -b main -q
git add .
git commit -am "Setup Nesta Data Science cookiecutter" -q
git checkout -b dev -q

echo "Configured git repo at $(pwd)"
