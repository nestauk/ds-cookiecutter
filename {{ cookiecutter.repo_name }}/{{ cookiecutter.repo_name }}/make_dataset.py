# -*- coding: utf-8 -*-
import logging
from dotenv import find_dotenv, load_dotenv
# Important to import the module
# This configures logging, file-paths, model config variables
import {{ cookiecutter.repo_name }}


logger = logging.getLogger(__name__)


def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """

    config = {{ cookiecutter.repo_name }}.config

    return


if __name__ == "__main__":
    # not used in this stub but often useful for finding various files
    project_dir = {{ cookiecutter.repo_name }}.project_dir

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    try:
        msg = f"Making datasets..."
        logger.info(msg)
        main()
    except (Exception, KeyboardInterrupt) as e:
        logger.exception("make_dataset failed", stack_info=True)
        raise e
