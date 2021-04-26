"""{{cookiecutter.repo_name }}."""
from setuptools import find_packages
from setuptools import setup


def read_lines(path):
    """Read lines of `path`."""
    with open(path) as f:
        return f.read().splitlines()


setup(
    name="{{ cookiecutter.repo_name }}",
    long_description=open("README.md").read(),
    install_requires=read_lines("requirements.txt"),
    extras_require={"dev": read_lines("requirements_dev.txt")},
    packages=find_packages(exclude=["docs"]),
    version="0.1.0",
    description="{{ cookiecutter.description }}",
    author="{{ cookiecutter.author_name }}",
    license="{% if cookiecutter.openness == 'public' %}MIT{% else %}proprietary{% endif %}",
)
