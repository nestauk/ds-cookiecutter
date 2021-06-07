"""Utils."""
import importlib
import inspect
import logging
from os import PathLike
from pathlib import Path

from metaflow import FlowSpec

from flowrider import REPO_NAME, SRC_DIR

logger = logging.getLogger(__file__)


def run_id_path(path: str, tag: str) -> Path:
    """Construct path to run id for flow corresponding to `{path}_{tag}`."""
    return SRC_DIR / "config" / "pipeline" / f"{path}_{tag}.run_id"


def load_run_id(path) -> int:
    """Load run id from `path`."""
    return int(path.open().read())


def flow_name_from_path(path: str) -> str:
    """Find the name of the flow corresponding to `path`."""
    flow_path = f"{REPO_NAME}.pipeline.{path}"

    # Import flow module
    module = importlib.import_module(flow_path)

    # Find subclass of metaflow.FlowSpec
    flows = inspect.getmembers(
        module, lambda obj: inspect.isclass(obj) and issubclass(obj, FlowSpec)
    )
    assert len(flows) == 1, f"More than one flow found in {module}"

    flow_name, _ = flows[0]
    return flow_name


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