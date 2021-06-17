# Quickstart

## Requirements

=== "Summary"

    -   A \*NIX system (e.g. Linux/macOS) - Windows might work, but we don't support it
        -   Mac users should also install [homebrew](https://brew.sh/) and [GNU coreutils](https://www.gnu.org/software/coreutils)
    -   [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
    -   [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0:
    -   [git-crypt](https://github.com/AGWA/git-crypt) - required for metaflow on AWS

    -   [github CLI](https://github.com/cli/cli) - for automatic creation and configuration of a Github repo
    -   Have a Nesta AWS account configured with `awscli`

=== "Installation and configuration help"

    -   A \*NIX system (e.g. Linux/macOS) - Windows might work, but we don't support it
        -   Mac users should also install:
            -   [homebrew](https://brew.sh/)
            -   [GNU coreutils](https://www.gnu.org/software/coreutils) - `brew install coreutils`.
    -   [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
    -   [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0:

        ```bash
        pip install cookiecutter  # might be pip3 on your machine
        ```

    -   [git-crypt](https://github.com/AGWA/git-crypt) - required for metaflow on AWS

        ```bash
        brew install git-crypt  # Mac
        apt-get install -y git-crypt  # Ubuntu linux
        ```

    -   [github CLI](https://github.com/cli/cli) - for automatic creation and configuration of a Github repo
        -   **Install**
            -   Mac: `brew install gh`
            -   Linux: [see instructions](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)
        -   **Configure** - `gh auth login` and answer prompts as below:
            -   _What account do you want to log into?_ **Github.com**
            -   _What is your preferred protocol for Git operations?_ **SSH**
            -   _Upload your SSH public key to your Github account?_ Select the key you used to sign-up for 2-factor authentication with github
            -   _How would you like to authenticate GitHub CLI?_ **Login with a web browser**

    -   [AWS CLI](https://aws.amazon.com/cli/) installed and configured to use a Nesta AWS account
        - **Install** - `pip install awscli`
        - **Configure**

            Fetch (or generate) [security credentials from the AWS dashboard](https://console.aws.amazon.com/iam/home?#security_credential) by clicking "Create access key".

            Run `aws configure`, inputting the access key ID and secret access key ID you just generated when prompted.

            In addition you should set the default region name to `eu-west-2` and the default output format to `None`.

            AWS provide a more detailed guide [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config).

## Starting from scratch

<!-- [![asciicast](https://asciinema.org/a/XYp6l2hknMVWWPbI76Qq8BTiq.svg){ height=30 }](https://asciinema.org/a/XYp6l2hknMVWWPbI76Qq8BTiq) -->

![asciicast](https://asciinema.org/a/XYp6l2hknMVWWPbI76Qq8BTiq.svg){ class=ascii }

### Create

Ensure you have installed the [requirements](#requirements) and then run `cookiecutter https://github.com/nestauk/ds-cookiecutter`.

This opens a series of prompts to configure your new project (values in square brackets denote defaults).

??? info "What do the prompts mean?"

    -   `project_name`: Type the name of your project here
    -   `repo_name`: Type the name of your repository here
        -   The default is a processed version of `project_name` that is compatible with python package names
    -   `author_name`: The author of the project
    -   `description`: A short description of your project
    -   `openness`: Whether the project is "public" (default) or "private"
        -   You should only make a project private if you have a good reason
        -   If "public" then an MIT license will be generated; otherwise the license will be a copyright placeholder
        -   A Github repo obeying this setting will be created for you in the next section
    -   `s3_bucket`: The name of an S3 bucket to store assets for this project
        -   This bucket will be created for you in the next section
        -   **Careful**: This needs to not conflict with any existing s3 bucket name and [S3 bucket names](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html) must only contain lowercase letters, numbers, dots, and hyphens.
        -   This value can be reconfigured in `.env.shared`
    -   `github_account`: The github account that this project will be created in

### Configure

Run `make init` to perform the following steps:

-   `install` - Required by everyone (creator and collaborators) this is itself composed of several sub-steps:

    -   `conda-create` - Create a conda environment, `project_name`, and install the project package in editable mode and its dependencies
    -   `setup-git` - Git pre-commit hooks have been configured and installed

        !!! warning inline end "Requires access to Nesta's AWS account"

    -   `setup-metaflow` - The Nesta metaflow config has been fetched and decrypted.
        It should exist in `~/.metaflowconfig/config_ds-cookiecutter.json`

-   `setup-github` - A github repo `github.com/nestauk/project_name` has been created and configured
-   `setup-bucket` - An s3 bucket `project_name` has been created

If you don't need a github repo or S3 bucket just run `make install`, you can always run the individual `make` commands later.

When you change directory to your created project folder, you will see that you are in a git branch `0_setup_cookiecutter`.
Make any tweaks to the cookiecutter required by your project ([see FAQ](../faq/#what-customisations-can-i-make-when-setting-up-the-cookiecutter-without-defeating-the-point-of-having-a-standard-project-template)), commit, and then make a Pull Request to `dev`.

## Collaborating on an existing project

-   Clone the repository and `cd` into the repository.
-   Run `make install` to configure the development environment (see above section)
-   Check the project's `README` for any additional configuration needed (e.g. putting API keys in `.env`)
-   Pull any required inputs into `inputs/` by running `make inputs-pull`
-   Follow the author's documentation, or make them write some if they haven't already!

## How can I use this if I don't have AWS?

If you don't have access to an AWS account you can still use the cookiecutter, you just need to remove a few bits relating to our AWS setup:

-   Remove the `setup-metaflow` dependency of the `install` recipe within `Makefile`
-   Remove the call to `setup-bucket` of the `init` recipe within `Makefile`
-   Remove the `inputs-push` and `inputs-pull` recipes within `Makefile`

If you're not using AWS then you do not require `awscli` and `gitcrypt` from the [requirements](#requirements).
