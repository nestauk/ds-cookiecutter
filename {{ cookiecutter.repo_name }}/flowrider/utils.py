"""Utils."""
import subprocess
import sys
from pathlib import Path


def load_run_id(path: Path) -> int:
    """Load run id from `path`."""
    return int(path.open().read())


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
