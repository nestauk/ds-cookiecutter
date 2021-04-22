from setuptools import find_packages, setup

setup(
    name="{{ cookiecutter.repo_name }}",
    packages=find_packages(),
    version="0.1.0",
    description="{{ cookiecutter.description }}",
    author="{{ cookiecutter.author_name }}",
    license="{% if cookiecutter.openness == 'public' %}MIT{% else %}proprietary{% endif %}",
)
