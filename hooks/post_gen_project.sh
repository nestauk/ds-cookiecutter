#!/bin/bash

# Create git repo
git init -q

# Setup empty master and dev
git checkout -b master -q
git commit --allow-empty -m "Initial commit." -q
git checkout -b dev -q

## Add cookiecutter on new branch
# Issue numbers don't start at zero so this won't conflict
export REPO_NAME="{{ cookiecutter.repo_name }}"
git checkout -b 0_setup_cookiecutter  -q
git add .
# Don't add example flows
git restore --staged \
"$REPO_NAME/pipeline/example/example_flow.py" \
"$REPO_NAME/getters/example.py" \
"$REPO_NAME/config/pipeline/example/example_flow_local.yaml"
git commit -am "Setup Nesta Data Science cookiecutter" -q

echo Configured git repo at $(pwd)

# Do everything if configured
if [ {{ cookiecutter.auto_config }} == "true" ]
then
    make init
else
    echo "You did not select auto_config, please enter the project directory & run 'make init' manually"
fi
