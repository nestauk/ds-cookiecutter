#!/bin/bash

PYTHON_VERSION="{{ cookiecutter.python_version }}"
VENV_TYPE="{{ cookiecutter.venv_type }}"
MODULE_NAME="{{ cookiecutter.module_name }}"
FILE_STRUCTURE="{{ cookiecutter.file_structure }}"
AUTOSETUP="{{ cookiecutter.autosetup }}"
USE_DIRENV="{{ cookiecutter.use_direnv }}"

# Different validation logic based on venv_type
if [ "$VENV_TYPE" = "uv" ]; then
    # For uv, check if version begins with == or >=
    if [[ "$PYTHON_VERSION" =~ ^(>=|==)3\.[0-9]+(\.([0-9]+|\*)){0,1}$ ]]; then
        : # Valid python version constraint for uv - already has prefix
    # If it's just a minor version like 3.10, add == prefix and wildcard
    elif [[ "$PYTHON_VERSION" =~ ^3\.[0-9]+$ ]]; then
        PYPROJECT_VERSION="==$PYTHON_VERSION.*"
        sed -i.bak "s/requires-python = \"$PYTHON_VERSION\"/requires-python = \"$PYPROJECT_VERSION\"/" pyproject.toml
        rm pyproject.toml.bak
    # If it's a patch version like 3.10.2, add == prefix
    elif [[ "$PYTHON_VERSION" =~ ^3\.[0-9]+\.[0-9]+$ ]]; then
        PYPROJECT_VERSION="==$PYTHON_VERSION"
        sed -i.bak "s/requires-python = \"$PYTHON_VERSION\"/requires-python = \"$PYPROJECT_VERSION\"/" pyproject.toml
        rm pyproject.toml.bak
    else
        echo "Error: For uv, python_version must be a valid version number (e.g. '3.10', '3.10.2') or have a prefix (e.g. '>=3.10', '==3.10.2')."
        exit 1
    fi
elif [ "$VENV_TYPE" = "venv" ]; then
    # For venv, require installed Python minor version format (3.x only)
    if [[ "$PYTHON_VERSION" =~ ^3\.[0-9]+$ ]]; then
        # Check if this Python version is installed
        if ! command -v "python$PYTHON_VERSION" >/dev/null 2>&1; then
            echo "Error: Python $PYTHON_VERSION not found in PATH. Make sure it's installed."
            exit 1
        fi
        PYPROJECT_VERSION="==$PYTHON_VERSION.*"
        sed -i.bak "s/requires-python = \"$PYTHON_VERSION\"/requires-python = \"$PYPROJECT_VERSION\"/" pyproject.toml
        rm pyproject.toml.bak
        sed -i.bak "s/\[dependency-groups\]/\[project.optional-dependencies\]/" pyproject.toml
        rm pyproject.toml.bak
    else
        echo "Error: For venv, python_version must be a minor version number only (e.g. '3.10', not '3.10.2')."
        exit 1
    fi
else  # conda
    # For conda, allow format (3.x or 3.x.y)
    if [[ "$PYTHON_VERSION" =~ ^3\.[0-9]+$ ]]; then
        PYPROJECT_VERSION="==$PYTHON_VERSION.*"
    elif [[ "$PYTHON_VERSION" =~ ^3\.[0-9]+\.[0-9]+$ ]]; then
        PYPROJECT_VERSION="==$PYTHON_VERSION"
    else
        echo "Error: For conda, python_version must be a plain version number (e.g. '3.10' or '3.10.2')."
        exit 1
    fi
    sed -i.bak "s/requires-python = \"$PYTHON_VERSION\"/requires-python = \"$PYPROJECT_VERSION\"/" pyproject.toml
    rm pyproject.toml.bak
    sed -i.bak "s/\[dependency-groups\]/\[project.optional-dependencies\]/" pyproject.toml
    rm pyproject.toml.bak
fi

# Remove environment.yaml if not using conda and docs if not included
# Set path, trim whitespace, and then remove if it exists
path='{% if cookiecutter.venv_type != "conda" %} environment.yaml {% endif %}'
path=$(echo "$path" | xargs)
if [ -n "$path" ] && [ -e "$path" ]; then
    rm "$path"
fi

if [ "$FILE_STRUCTURE" = "simple" ]; then
    rm -rf docs
    rm -rf tests
    rm -rf "$MODULE_NAME/config"
    rm -rf "$MODULE_NAME/utils"
    rm -rf "$MODULE_NAME/pipeline"
    mv "$MODULE_NAME/analysis/notebooks" "$MODULE_NAME/"
elif [ "$FILE_STRUCTURE" = "standard" ]; then
    rm -rf docs
    rm -rf tests
fi

if [ "$USE_DIRENV" = "yes" ]; then
    if command -v direnv &> /dev/null; then
        echo
        echo "Authorizing direnv..."
        direnv allow
    else
        echo
        echo "Note: direnv is not installed. Install it to automatically activate your environment when entering the directory."
    fi
else
    rm -f .envrc
fi

if [ "$AUTOSETUP" = "no" ]; then
    echo "Auto setup is disabled. Finished."
    exit 0
fi

# Create git repo
git init -q
git add .

echo
echo "Setting up virtual environment and installing dependencies..."
if [ "$VENV_TYPE" = "uv" ]; then
    uv sync
    source .venv/bin/activate
elif [ "$VENV_TYPE" = "venv" ]; then
    python$PYTHON_VERSION -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install ".[dev]"
elif [ "$VENV_TYPE" = "conda" ]; then
    # Check if conda is initialized in the current shell
    if ! command -v conda &> /dev/null; then
        echo "Error: conda command not found. Please ensure conda is installed and initialized."
        echo "You may need to run 'conda init bash' (or your shell) and restart your terminal."
        exit 1
    fi
    # Check if the environment already exists
    if conda env list | grep -q "^$MODULE_NAME "; then
        echo "Warning: conda environment '$MODULE_NAME' already exists."
        if [[ -t 0 ]]; then
            read -p "Do you want to remove it and create a new one? (y/N) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo "Removing existing environment..."
                conda env remove -n "$MODULE_NAME" -y
            else
                echo "Aborting setup. Please choose a different project name or remove the existing environment."
                exit 1
            fi
        else
            echo "Non-interactive mode: auto-removing environment."
            conda env remove -n "$MODULE_NAME" -y
        fi
    fi
    conda env create -f environment.yaml -n "$MODULE_NAME"
    eval "$(conda shell.bash hook)"
    conda activate "$MODULE_NAME"
    pip install ".[dev]"
fi

echo
echo "Setting up pre-commit hooks..."

pre-commit install --install-hooks
pre-commit run pre-commit-update
git add .pre-commit-config.yaml
pre-commit run prettier
git add .pre-commit-config.yaml

# Deactivate the virtual environment
if [ "$VENV_TYPE" = "uv" ] || [ "$VENV_TYPE" = "venv" ]; then
    deactivate
elif [ "$VENV_TYPE" = "conda" ]; then
    conda deactivate
fi

echo "Setting up git branches and making initial commit..."
git checkout -b main -q
git add .
SKIP=no-commit-to-branch git commit -am "Setup Nesta Data Science cookiecutter"
git checkout -b dev -q

# # Set up remote using the module_name
# REPO_URL="git@github.com:nestauk/$MODULE_NAME.git"

# # Ask about force pushing
# read -p "Do you want set up the remote (pointing at $REPO_URL) and force push? The repository must already exist. This will overwrite any existing branches with the contents of the cookiecutter. (y/N) " -n 1 -r FORCE_REPLY
# echo

# if [[ $FORCE_REPLY =~ ^[Yy]$ ]]; then
#     echo
#     echo "WARNING: This operation will overwrite any existing work in the repository."
#     read -p "Are you sure you want to force push? (y/N) " -n 1 -r CONFIRM_REPLY
#     echo
#     if [[ $CONFIRM_REPLY =~ ^[Yy]$ ]]; then
#         echo "Force pushing branches to remote..."
#         git remote add origin "$REPO_URL"
#         git push -f origin main
#         git push -f origin dev
#     else
#         echo "Not pushing to remote. You can manually add the remote later with the following command:"
#         echo "git remote add origin $REPO_URL"
#         echo
#     fi
# else
#     echo "Not pushing to remote. You can add the remote manually later with the following command:"
#     echo "git remote add origin $REPO_URL"
#     echo
# fi

echo "Successfully configured git repo at $(pwd)"
echo


echo "Setup complete! You can now start working on your project."
