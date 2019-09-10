#!/bin/bash 

# git filter to strip notebooks of output
config="[filter \"nbstrip_full\"]\n clean = \"jq --indent 1 '(.cells[] | select(has(\\\"outputs\\\")) | .outputs) = []  | (.cells[] | select(has(\\\"execution_count\\\")) | .execution_count) = null  | .metadata = {\\\"language_info\\\": {\\\"name\\\": \\\"python\\\", \\\"pygments_lexer\\\": \\\"ipython3\\\"}} | .cells[].metadata = {} '\"\n smudge = cat\n required = true\n "

git init  # Create git repo
echo -e $config >> .git/config  # Copy git filter

git add .
git add data/raw -f
git add data/interim -f
git commit -am"Setup Nesta Data Science cookiecutter"


