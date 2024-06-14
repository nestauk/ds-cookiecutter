# {{cookiecutter.project_name}}

**_Change this to the full project name 👆_**

**_Add a one-liner that describes this project._**

## 👋 Welcome!

**_Write a longer description of the project here. Put what you like here, but you might want to include:_**

- **_Some background on the project and what its aims are_**
- **_A high level description of what the code in this repository does_**
- **_Links to other relevant work or information on Nesta's website_**
- **_The respository's development status. Is this currently under development, finished, parked (offer an explanation if you feel it is needed)._**
- **_Link to any particularly important project outputs:_**
  - **_reports_**
  - **_slide decks_**
  - **_media_**

![Maybe add an image or nice graphic relating to the project here. This one is by Alan Warburton / © BBC / Better Images of AI / Plant / CC-BY 4.0](https://betterimagesofai.org/ImagesAI/WarburtonNature_01_1280x720.jpg)

## 📂 Contents

**_Write a high level outline of the repository contents and structure. What are the main functions and outputs and where can the reader find them? This is not a replacement for informative readmes in sub-directories!_**

## 🛠️ Setup and installation

**Step 1.** Check that you meet the [data science cookiecutter requirements](http://nestauk.github.io/ds-cookiecutter/quickstart). In brief:

Install the following components:

- [gh](https://formulae.brew.sh/formula/gh) - GitHub command line tool.
- [direnv](https://formulae.brew.sh/formula/direnv#default) - For using environment variables.
- [git-crypt](https://github.com/AGWA/git-crypt/blob/master/INSTALL.md#installing-on-mac-os-x) - Tool for encryption of sensitive files.

Have a Nesta AWS account, and install and configure your [AWS Command Line Interface](https://docs.aws.amazon.com/polly/latest/dg/setup-aws-cli.html)

**Step 2.** Setup other dependencies.

**_Are there any other dependencies that this project requires?_**

**Step 3.** Install, configure and activate the environment for this project on your machine.

Create a blank cookiecutter conda log file:

```
$ mkdir .cookiecutter/state
$ touch .cookiecutter/state/conda-create.log
```

Run `make install` to configure the development environment:

- Setup the conda environment
- Configure `pre-commit`

Activate the newly created conda environment with `conda activate {{ cookiecutter.project_name }}`

## 💾 Datasets

**_List and describe any datasets used in the project. If possible link to them or a page that describes them. If special requirements are needed to access them, this might be a good place to explain._**

## 🏁 Testing

**_If this project has tests, explain how to run them here._**

## 🤝 Contributor guidelines

[Nesta's technical and working style guidelines for data scientists](https://github.com/nestauk/ds-cookiecutter/blob/master/GUIDELINES.md)

## 📧 Get in touch

**_If you want people to reach out about the work, put relevant email addresses here or instructions on how to leave an issue (only do this if you expect that you or someone will respond)._**

---

<small><p>Project based on <a target="_blank" href="https://github.com/nestauk/ds-cookiecutter">Nesta's data science project template</a>
(<a href="http://nestauk.github.io/ds-cookiecutter">Read the docs here</a>).
</small>
