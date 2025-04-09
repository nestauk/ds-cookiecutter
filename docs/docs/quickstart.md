# Project Set Up

## Your Guide to Setting Up a Nesta Cookiecutter Project

In this page you will learn how to set up a project using the cookiecutter. The steps are different depending on whether you are the first one setting up a project ([Project Configurer](#project-configurer)) or whether a project already exists and you are just setting it up locally ([Team Member](#team-members)).

### Project Configurer

_**Prerequisite**: If this is your first time setting up a cookiecutter project you need to install it from https://pypi.org/project/cookiecutter. You can do this in the terminal with `brew install cookiecutter`._

1. **Request repository setup**: First things first, you need a repo created for you. From the [tech support website](https://nestagroup.atlassian.net/servicedesk/customer/portals), go to _Ask Nesta Technology_, _Request Forms_, then _Request GitHub repository_. You will need to provide a _project name_, _repo name_, whether _public/private_, _github teams involved_, _team leading the project_, _short and long description of the project_. An empty repo will automatically be set up for you within a few minutes: https://github.com/nestauk/your_repo_name. Your team should have admin access on the repository. 

2. **Set up your project locally**: It is important that you _do not clone the repo yet!_ Instead, follow these steps:

-   Open the terminal and `cd` to a folder where you eventually want your repo to be
-   Run `cookiecutter https://github.com/nestauk/ds-cookiecutter`. This will automatically install the latest version. If you want to install a different version run `cookiecutter https://github.com/nestauk/ds-cookiecutter -c <VERSION TAG>`
-   You will be presented with the following:

    -   `You've downloaded ~.cookiecutters/ds-cookiecutter before. Is it okay to delete and re-download it?[yes]` press Enter to confirm yes, it's always best to use the latest version.
    -   `project_name [Project_name]`: add_a_name_here
    -   `repo_name [add_a_name_here]`: add_a_name_here
    -   `author_name [Nesta]`: add_author or press Enter to confirm Nesta
    -   `description [A short description of the project.]`: add short description
    -   `Select openness: 1 - public 2 - private Choose from 1, 2 [1]`: regardless of the choice you can always change it in the future
    -   `Select venv_type: 1 - uv 2 - venv 3 - conda`: choose how you will manage your virtual environment

-  Setup your project directory as described in 

3. **Connect your local project to github**: You have set up your project locally and now you have to connect it to the remote repo. When you change directory to your created project folder, you will see that you are in a git repository and the generated cookiecutter has committed itself to the `main` and `dev` branches. Connect to the git repo by running `git remote add origin git@github.com:nestauk/<REPONAME>` to point your local project to the configured repository.

4. **You are all set!**

### Team Members

-   Open the terminal and `cd` into a folder where you want the project set up.
-   Clone the repository by running `git clone <REPONAME>` and `cd` into the repository.
-   Run `make install` to configure the development environment.
