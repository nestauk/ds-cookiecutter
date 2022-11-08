#!/bin/bash

#If a git repo already exists than don't create a new one
if [ -d "../{{ cookiecutter.repo_name }}/.git" ]
then
    # Add cookiecutter on new branch
    # Issue numbers don't start at zero so this won't conflict
    git checkout -b 0_setup_cookiecutter  -q
    git add .
    git commit -am "Setup Nesta Data Science cookiecutter" -q

    echo "Configured git repo at $(pwd), please enter the project directory & run 'make install'"

    # Permit auto-loading of .envrc
    direnv allow

else
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
fi
