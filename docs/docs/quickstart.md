# Project Set Up

## Your Guide to Setting Up a Nesta Cookiecutter Project

In this page you will learn how to set up a project using the cookiecutter. The steps are different depending on whether you are the first one setting up a project (Project Configurer) or whether a project already exists and you are just setting it up locally (Team Member).

=== "Project Configurer"

    -   *Request repository setup*: First things first, you need a repo created for you. Submit a [Create a repo in the Nesta GitHub org](https://github.com/nestauk/github_support/issues/new/choose) issue from the [github_support](https://github.com/nestauk/github_support) issue page. You will need to provide a project name, suggested repo name, whether public/private, github teams involved, team leading the project, short and long description of the project. An empty repo will be set up for you and you will receive a notification when this is done.
    -   *Set up project locally*: It is important that you do not clone the repo yet! Instead, follow these steps:
        -   Open the terminal
        -   `cd` to a folder where you eventually want your repo to be
        -   run `cookiecutter https://github.com/nestauk/ds-cookiecutter`. This will automatically install the latest version. If you want to install a different version run `cookiecutter https://github.com/nestauk/ds-cookiecutter -c <VERSION TAG>`
        - You will be presented with the following:
        - `You've downloaded ~.cookiecutters/ds-cookiecutter before. Is it okay to delete and re-download it?[yes]` press Enter to confirm yes
        - project_name [Project_name]: add_a_name_here
        - repo_name [add_a_name_here]: add_a_name_here
        - author_name [Nesta]: add_author
        - description [A short description of the project.]: add short description
        - Select openness:
            1 - public
            2 - private
            Choose from 1, 2 [1]: regardless of the choice you can always change it in the future by speaking with a DE colleague

        - `cd` to project directory and run `make install` to:
            - Create a conda environment (with a name corresponding to the repo_name prompt) and install the project package in editable mode and its dependencies
            - Configure and install Git pre-commit hooks
        - When you change directory to your created project folder, you will see that you are in a git repository and the generated cookiecutter has committed itself to the `0_setup_cookiecutter` branch.
        - Connect to git repo: Run `git remote add origin git@github.com:nestauk/<REPONAME`  to point your local project to the configured repository
        - Merge the new branch to `dev` by running

        ``` bash

            git checkout 0_setup_cookiecutter
            git branch dev 0_setup_cookiecutter -f
            git checkout dev
            git push origin dev -f
            ```
        - You are all set! You can delete the `0_setup_cookicutter` branch


=== "Team Members"

    - Clone the repository by running `git clone <REPONAME>` and `cd` into the repository.
    - Run `make install` to configure the development environment 

  
