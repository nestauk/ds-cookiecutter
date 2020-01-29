# Quickstart

## Starting from scratch

### Create cookiecutter

- `pip install cookiecutter`
- `cookiecutter https://github.com/nestauk/cookiecutter-data-science-nesta`
  This opens a series of prompts to configure your new project (values in square brackets denote defaults):
  - `project_name [project_name]:` Type the name of your project here
  - `repo_name [project_name]:` Type the name of your repository here
  - `author_name [Nesta]:` The author of the project (you or your organisation)
  - `description [...]:` A short description of your project
  - `Select open_source_license: ...` Choose the license you wish to use 
  - `s3_bucket ...:` The name of an S3 bucket to sync your raw data to
  - `aws_profile [default]:` The AWS profile name to use for syncing to S3. Choose default unless your an advanced user.
- `cd <repo_name>`

### Create a virtual environment

- Add any libraries you know you will need into `conda_environment.yaml`
- Run `make create_environment` - This will setup a conda environment named according to your repository, and install your project as a local, editable package
- `conda activate <environment name>` (`conda env list` will list available environments if you're unsure what your environment is called)

### First step

We've setup our project structure and environment, now you're ready to get going!

The best first step is to write `<repo_name>/fetch_data.py` to fetch all your data, and store it in `data/raw/`.

`make fetch` will run this file and sync `data/raw` to s3 for you (as long as you setup a bucket).

## Reproducing someone else's work

- Clone the repository and `cd` into the repository.
- Run `make create_environment` - This will setup a conda environment named according to your repository, and install your project as a local, editable package.
- `conda activate <environment name>` will activate the environment (`conda env list` will list available environments if you're unsure what your environment is called)
- Check the README for any configuration needed (e.g. putting API keys in `.env`)
- Get the raw data: `make sync_from_s3`
- Follow their documentation, or make them write some if they haven't already!