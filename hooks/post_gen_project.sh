#!/bin/bash

# Create git repo
git init -q

# Setup empty master and dev
git checkout -b master -q
git commit --allow-empty -m "Initial commit." -q
git checkout -b dev -q

# Add cookiecutter on new branch
# Issue numbers don't start at zero so this won't conflict
git checkout -b 0_setup_cookiecutter  -q
git add .
git commit -am "Setup Nesta Data Science cookiecutter" -q

echo "Configured git repo at $(pwd), please enter the project directory & run 'make install'"

# Permit auto-loading of .envrc
direnv allow

# Remove environment.yaml if not using conda
# Set path, trim whitespace, and then remove if it exists
path='{% if cookiecutter.venv_type != "conda" %} environment.yaml {% endif %}'
path=$(echo "$path" | xargs)
if [ -n "$path" ] && [ -e "$path" ]; then
    rm "$path"
fi
