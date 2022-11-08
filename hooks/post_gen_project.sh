#!/bin/bash

# Add cookiecutter on new branch
# Issue numbers don't start at zero so this won't conflict
git checkout -b 0_setup_cookiecutter  -q
git add .
git commit -am "Setup Nesta Data Science cookiecutter" -q

echo "Configured git repo at $(pwd), please enter the project directory & run 'make install'"

# Permit auto-loading of .envrc
direnv allow
