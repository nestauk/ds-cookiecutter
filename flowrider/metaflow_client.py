"""Utils to get and cache the results of metaflows."""
import importlib
import inspect
import logging
from pathlib import Path
from typing import Any, Callable, Optional

from metaflow import FlowSpec, Run
from toolz import compose_left, identity

from flowrider import REPO_NAME, SRC_DIR
from flowrider.cache import cache_getter_fn

logger = logging.getLogger(__file__)

__all__ = ["auto_getter"]


def auto_getter(
    path: str,
    tag: str,
    artifact: str,
    cache_strategy: Optional[Callable] = cache_getter_fn,
) -> Any:
    """Return flow object based on `path` and `tag`.

    - Loads `run_id` from `config/pipeline/{path}_{tag}.run_id
    - Introspects name of flow

    Args:
        path:
        tag:
        cache_strategy: Decorator to cache artifact with, if `None` no caching.

    Returns:
        Metaflow data artifact
    """
    run_id = compose_left(run_id_path, load_run_id)(path, tag)
    flow_name = flow_name_from_path(path)

    if cache_strategy is None:
        cache_strategy = identity

    @cache_strategy
    def get(flow_name, run_id, artifact):
        return getattr(Run(f"{flow_name}/{run_id}").data, artifact)

    return get(flow_name, run_id, artifact)


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
