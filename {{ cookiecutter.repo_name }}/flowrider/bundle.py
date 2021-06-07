"""Bundle."""
import shutil
from functools import partial
from os import PathLike
from pathlib import Path
from tempfile import mktemp
from typing import Collection, Iterable, List

from flowrider.utils import is_dir

__all__ = ["bundle"]


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
        ignore=partial(_ignore, allowed_suffixes=allowed_suffixes),
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


def _ignore(
    src: PathLike,
    names: Iterable[str],
    allowed_suffixes: Collection[str],
) -> List[str]:
    """Return from `names` sub-directories of `src` or files with allowed_suffixes."""

    def include(x):
        return is_dir(src, x) or any(map(x.endswith, allowed_suffixes))

    return [x for x in names if not include(x)]
