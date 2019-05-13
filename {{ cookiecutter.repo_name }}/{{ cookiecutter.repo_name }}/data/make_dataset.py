# -*- coding: utf-8 -*-
import click
import logging
from dotenv import find_dotenv, load_dotenv
# Important to import the module
# This configures logging, file-paths, model config variables
import {{ cookiecutter.repo_name }}


@click.command()
@click.argument('arg', type=str)
@click.option('-o', '--opt', default=None, type=int)
def main(arg, opt):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).

    Usage: `python make_dataset.py arg -o opt`

    Args:
        arg (str):
            Required command line argument.
        opt (int, optional):
            Command line option.
            Set with `-o` or `--opt`.
            Defaults to None.
    """
    logger = logging.getLogger(__name__)

    try:
        msg = f'making final data set from raw data with: arg={arg}; opt={opt}'
        logger.info(msg)
    except (Exception, KeyboardInterrupt) as e:
        logger.exception('make_dataset ({arg}, {opt}) failed', stack_info=True)
        raise e


if __name__ == '__main__':
    # not used in this stub but often useful for finding various files
    project_dir = {{ cookiecutter.repo_name }}.project_dir

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
