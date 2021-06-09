"""Utils."""
import logging
import subprocess
import sys
from os import PathLike
from pathlib import Path


logger = logging.getLogger(__file__)

# GENERIC
def load_run_id(path: Path) -> int:
    """Load run id from `path`."""
    return int(path.open().read())


def is_dir(src: PathLike, x):
    """Is `x` a directory child of `src`?."""
    return (Path(src) / x).is_dir()


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
