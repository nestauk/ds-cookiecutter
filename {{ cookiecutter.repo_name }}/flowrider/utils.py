"""Utils."""
import importlib
import inspect
import logging
import subprocess
import sys
from os import PathLike
from pathlib import Path

from metaflow import FlowSpec

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


# COOKIECUTTER - getter
def run_id_path(flow_subpath: str, tag: str, src_dir: Path) -> Path:
    """Construct path to run id for flow corresponding to `{path}_{tag}`.

    E.g. "myflow/flow"
    """
    return src_dir / "config" / "pipeline" / f"{flow_subpath}_{tag}.run_id"


def flow_name_from_path(flow_subpath: str, repo_name: str) -> str:
    """Find the name of the flow corresponding to `path`."""
    flow_module = f"{repo_name}.pipeline.{flow_subpath}"

    # Import flow module
    module = importlib.import_module(flow_module)

    # Find subclass of metaflow.FlowSpec
    # TODO Make this less brittle!
    flows = inspect.getmembers(
        module,
        lambda obj: (inspect.isclass(obj) and issubclass(obj, FlowSpec))
        or (
            hasattr(obj, "__wrapped__")
            and inspect.isclass(obj.__wrapped__)
            and issubclass(obj.__wrapped__, FlowSpec)
        ),
    )
    assert len(flows) == 1, f"Expected one flow in {module}, found {len(flows)}"

    flow_name, _ = flows[0]
    return flow_name
