# Quickstart

## Requirements

=== "Summary"

    -   A \*NIX system (e.g. Linux/macOS) - Windows might work, but we don't support it
        -   Mac users should also install [homebrew](https://brew.sh/) and [GNU coreutils](https://www.gnu.org/software/coreutils)
    -   [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
    -   [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0:
    - [direnv](https://direnv.net/docs/installation.html) - Automatically loads environment variables and environments
    - Optional: [AWS CLI](https://aws.amazon.com/cli/) installed and configured
        -   Needed to use S3 for data storage

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
    - [direnv](https://direnv.net/docs/installation.html) - Automatically loads environment variables and environments
        ```bash
        brew install direnv  # Mac
        apt-get install -y direnv  # Ubuntu Linux
        ```
        Add `eval "$(direnv hook $SHELL)"` at the end of your `~/.${SHELL}rc` file.
    - Optional: [AWS CLI](https://aws.amazon.com/cli/) installed and configured
        - **Install** - `pip install awscli`
        - **Configure**

            Fetch (or generate) [security credentials from the AWS dashboard](https://console.aws.amazon.com/iam/home?#security_credential) by clicking "Create access key".

            Run `aws configure`, inputting the access key ID and secret access key ID you just generated when prompted.

            In addition you should set the default region name to `eu-west-2` and the default output format to `json`.

            AWS provide a more detailed guide [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config).

### Create

Ensure you have installed the [requirements](#requirements) and then run `cookiecutter https://github.com/nestauk/ds-cookiecutter -c <VERSION TAG>`.

??? attention "If you do not specify a version tag then `cookiecutter` will use the latest commit on the `master` branch. Unless specifying a version you have used before, check the [release notes](https://github.com/nestauk/ds-cookiecutter/releases) to see what changed since you last created a project!"

    Currently, only the latest release's docs are available online.
    You can serve docs for a specific release on your machine by checking out that release and running `pip install -r requirements.txt && cd docs && mkdocs serve` and then navigating to `localhost:8000` in your browser.

This opens a series of prompts to configure your new project (values in square brackets denote defaults).

??? info "What do the prompts mean?"

    -   `project_name`: Type the name of your project here
    -   `repo_name`: Type the name of your repository here
        -   The default is a processed version of `project_name` that is compatible with python package names
    -   `author_name`: The author of the project
    -   `description`: A short description of your project
    -   `openness`: Whether the project is "public" (default) or "private"
        -   If "public" then an MIT license will be generated; otherwise the license will be a copyright placeholder

### Configure

When you change directory to your created project folder, you will see that you are in a git repository and the generated cookiecutter has committed itself to the `0_setup_cookiecutter` branch.

Run `make install` to:

-   Create a conda environment (with a name corresponding to the `repo_name` prompt) and install the project package in editable mode and its dependencies
-   Configure and install Git pre-commit hooks

Now you're setup, you may wish to adapt the cookiecutter to fill your specific needs, e.g. by looking at other components in [`.recipes/`](https://github.com/nestauk/ds-cookiecutter/blob/master/%7B%7B%20cookiecutter.repo_name%20%7D%7D/.recipes) ([see FAQ](../faq/#what-customisations-can-i-make-when-setting-up-the-cookiecutter-without-defeating-the-point-of-having-a-standard-project-template)).

## Collaborating on an existing project

-   Clone the repository and `cd` into the repository.
-   Run `make install` to configure the development environment (see above section)
    - Troubleshooting this step: This step frequently causes a `.cookiecutter/state/` error, which can usually be solved by running `mkdir -p .cookiecutter/state/ && touch .cookiecutter/state/conda-create.log` from the root of the directory prior running `make install`
-   Check the project's `README` for any additional configuration needed (e.g. putting API keys in `.env`)
    -   Ideally that projects maintainer will have extended the `Makefile` to do additional configuration automatically
-   Follow the author's documentation, or make them write some if they haven't already!
