# Quickstart

## Requirements

- Python 3.6+
- A \*NIX system (e.g. Linux/macOS) - Windows might work, but we don't support it
    - Mac users: The commands below assume you have [homebrew](https://brew.sh/) installed
- [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0:
```bash
pip install cookiecutter
```
- [git-crypt](https://github.com/AGWA/git-crypt) - required for metaflow on AWS
```bash
brew install git-crypt  # mac
apt-get install -y git-crypt  # Ubuntu linux:
```
- [github CLI](https://github.com/cli/cli) [**OPTIONAL** - required if `auto_config` set to true (the default)] - for automatic creation and configuration of a Github repo

    - **Install**
        - Mac: `brew install gh`
        - Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md
    - **Configure**: `gh auth login` and answer prompts as below:
        - *What account do you want to log into?* **Github.com**
        - *What is your preferred protocol for Git operations?* **SSH**
        - *Upload your SSH public key to your Github account?* Select the key you used to sign-up for 2-factor authentication with github
        - *How would you like to authenticate GitHub CLI?* **Login with a web browser**

- Have a Nesta AWS account configured with `awscli`
    - **Note to any non-Nesta visitors:** You can still use the cookiecutter by:
        * Choosing `auto_config` as "false" when setting up the cookiecutter
        * Remove the `setup-metaflow` dependency of the `install` command within `Makefile`
        * If using `make init` - replace references to `nestauk` with your github organisation in `bin/create_repo.sh`

We recommend taking the time to install and configure the optional dependencies as this one-time setup allows you to use the `auto_config` option which should save you a lot of time and avoids human error during configuration.

## Starting from scratch

### Create

Ensure you have installed the [requirements](#Requirements) and then run `cookiecutter https://github.com/nestauk/ds-cookiecutter`.

This opens a series of prompts to configure your new project (values in square brackets denote defaults):

- `project_name`: Type the name of your project here
- `repo_name`: Type the name of your repository here
    - The default is a processed version of `project_name` that is compatible with python package names
- `author_name`: The author of the project
- `description`: A short description of your project
- `openness`: Whether the project is "public" (default) or "private"
    - You should only make a project private if you have a good reason
    - If "public" then an MIT license will be generated; otherwise the license will be a copyright placeholder
    - If you choose `auto_config` as "true" then the Github repo created will obey this setting
- `s3_bucket`: The name of an S3 bucket to store assets for this project
    - If you choose `auto_config` as "true" then this bucket will be created for you
    - **Careful**: This needs to not conflict with any existing s3 bucket name
    - This value can be reconfigured in `.env.shared`
- `github_account`: The github account that this project will be created in
- `auto_config`: Whether to automatically create a conda environment; github repo; S3 bucket; and configure AWS with metaflow.
    - Requires optional requirement `gh` (the Github cli) to have been installed and configured (with `gh auth login`)

### Configure

- If you selected `auto_config` as "true", the following actions have happened:

    - A conda environment, `project_name`, has been created (with the project package installed in editable mode)
    - Git pre-commit hooks have been configured and installed
    - The Nesta metaflow config has been fetched and decrypted. It should exist in `~/.metaflowconfig/config.json`
    - A github repo `github.com/nestauk/project_name` has been created and configured
    - An s3 bucket `project_name` has been created

- If you selected `auto_config` as "false", you will need to do the above manually (or run `make init`):
    - Run `make install` to configure the development environment:
        - Setup the conda environment
        - Configure pre-commit
        - Configure metaflow to use AWS
    - Manually create an S3 bucket `s3_bucket` (or run `bash bin/create_bucket.sh`)

      [S3 names](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html) must only contain lowercase letters, numbers, dots, and hyphens.

    - Manually create a github repository (or run `bash bin/create_repo.sh`)

## Collaborating on an existing project

- Clone the repository and `cd` into the repository.
- Run `make install` to configure the development environment:
    - Setup the conda environment
    - Install dependencies and local package
    - Configure pre-commit
    - Configure metaflow to use AWS
- `conda activate project_name`
- Check the project's `README` for any additional configuration needed (e.g. putting API keys in `.env`)
- Pull any required inputs into `inputs/` by running `make inputs-pull`
- Follow the author's documentation, or make them write some if they haven't already!
