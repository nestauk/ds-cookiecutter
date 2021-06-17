"""Decorators."""
import functools
import logging
import subprocess
import sys
from typing import Any, Callable, Dict

from flowrider.utils import is_pkg_installed


def install_reqs(cls: Callable[..., Any]) -> Callable[[Callable[..., Any]], Any]:
    """Install local package."""

    @functools.wraps(cls)
    def inner(*args, **kwargs):
        # TODO: what if no setup.py exists (e.g. if not run with `flowrider` CLI)

        # If pkg not already installed (i.e. running in batch or meta-conda) then do it
        pkg_name = subprocess.getoutput(f"{sys.executable} setup.py --name")
        if not is_pkg_installed(pkg_name):
            logging.info(f"Installing `{pkg_name}` for {sys.executable}...")
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-e",
                    ".",
                    "--quiet",
                ],
                stdout=subprocess.DEVNULL,
                check=True,
            )
        else:
            logging.info(
                f"Not installing `{pkg_name}`"
                f" - already exists for environment {sys.executable}"
            )
        return cls(*args, **kwargs)

    return inner


def pip(libraries: Dict[str, str]) -> Callable[[Callable[..., Any]], Any]:
    """Install `libraries` with pip.

    Args:
        libraries: Keys are library names, values are version constraints.
            Value of `None` will not use a version constraint.
    """

    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):

            logging.info(f"In {sys.executable}...")
            for library, version in libraries.items():
                pkg = library + (version or "")
                logging.info(f"Pip Install: {pkg}")
                try:
                    subprocess.run(
                        [
                            sys.executable,
                            "-m",
                            "pip",
                            "install",
                            "--quiet",
                            pkg,
                        ],
                        check=True,
                        stdout=subprocess.DEVNULL,
                    )
                except subprocess.CalledProcessError as exc:
                    logging.error(f"Failed to install {pkg} with pip")
                    raise exc
            return function(*args, **kwargs)

        return wrapper

    return decorator
