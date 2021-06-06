import functools
import logging
import shutil
import subprocess
import sys
from functools import partial
from os import PathLike
from pathlib import Path
from tempfile import mktemp
from typing import Any, Callable, Collection, Dict, Iterable, List


def bundle(pkg_path: Path, flow_path: Path, allowed_suffixes: Collection[str]) -> Path:
    """Bundle

    Args:
        pkg_path: Path to package being bundled
        flow_path: Path to flow ...
        allowed_suffixes: File suffixes to bundle?

    Returns:
        Path package bundled at.
    """

    tmp_flow_path = Path(mktemp())

    # Copy local package
    shutil.copytree(
        f"{pkg_path}",
        f"{tmp_flow_path}",
        ignore=partial(ignore, allowed_suffixes),
    )

    # Copy flow to base of project such that package can be imported
    shutil.copy(flow_path, f"{tmp_flow_path}/{flow_path.name}")

    # TODO: what about local imports alongside flow?
    #  e.g. `from .utils import foo` from within a flow
    #
    #  Could do:
    #   shutil.copytree(flow_path.parent, tmp_flow_path, dirs_exist_ok=True)
    #  but that risks overwriting files!
    #  people should just use absolute imports / filepaths!

    return tmp_flow_path


def is_dir(src: PathLike, x):
    """Is `x` a directory child of `src`?."""
    return (Path(src) / x).is_dir()


def ignore(
    allowed_suffixes: Collection[str], src: PathLike, names: Iterable[str]
) -> List[str]:
    """Return from `names` sub-directories of `src` or files with allowed_suffixes."""

    def include(x):
        return is_dir(src, x) or any(map(x.endswith, allowed_suffixes))

    return [x for x in names if not include(x)]


def is_pkg_installed(pkg_name: str) -> bool:
    """Is `pkg_name` installed in running python environment?"""
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "show", pkg_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def son_of_a_batch(cls: object) -> Callable[[Callable[..., Any]], Any]:
    """Install local package."""

    @functools.wraps(cls)
    def inner(*args, **kwargs):
        # If pkg not already installed (i.e. running in batch or meta-conda) then do it
        # pkg_name = __package__.split(".")[0]
        pkg_name = subprocess.getoutput(f"{sys.executable} setup.py --name")
        if not is_pkg_installed(pkg_name):
            logging.info(f"Installing `{pkg_name}`...")
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


# %%


# import subprocess
# import sys

# library = "tqdm"
# version = "<0"
# try:
#     subprocess.run(
#         [
#             # sys.executable,
#             # "-m",
#             "pip",
#             "install",
#             # "--quiet",
#             library + (version or ""),
#         ],
#         check=True,
#     )
# except subprocess.CalledProcessError as e:
#     # print(e.args)
#     # print(e.returncode)
#     # print(e.output)
#     # print(e.stderr)
#     print(e.stdout)
#     o = e
