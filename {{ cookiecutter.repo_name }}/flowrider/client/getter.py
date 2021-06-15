"""Automaticaly generate artifact getters."""
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Optional

from metaflow import get_metadata, metadata, Run
from metaflow.client.core import Flow
from toolz import identity

from flowrider.client.cache import cache_getter_fn
from flowrider.config_parser import parse_config
from flowrider.utils import load_run_id


__all__ = ["auto_getter"]


def auto_getter(
    flow: Flow,
    config_subpath: str,
    artifact: str,
    module: ModuleType,
    cache_strategy: Optional[Callable] = cache_getter_fn,
) -> Any:
    """Return flow object based on `path` and `tag`.

    - Loads `run_id` from `config/pipeline/{path}_{tag}.run_id
    - Introspects name of flow

    Args:
        TODO
        cache_strategy: Decorator to cache artifact with, if `None` no caching.

    Returns:
        Metaflow data artifact
    """
    cache_strategy = cache_strategy or identity

    src_dir = Path(module.__file__).parent

    config_path = (src_dir / config_subpath).with_suffix(".yaml")
    config = parse_config(config_path)  # TODO: don't evaluate hooks!
    metadata = (
        f"local@{src_dir.parent}"  # Set specific local metadata directory
        if config["preflow_kwargs"].get("metadata", None) == "local"
        else get_metadata()
    )

    run_id_path = config_path.with_suffix(".run_id")
    run_id = load_run_id(run_id_path)

    @cache_strategy
    def get(flow_name, run_id, artifact):
        return getattr(Run(f"{flow_name}/{run_id}").data, artifact)

    with _metadata(metadata):
        return get(flow.__name__, run_id, artifact)


@contextmanager
def _metadata(ms):
    """Context manager to use Metaflow local metadata."""
    original_ms = get_metadata()
    metadata(ms)
    yield
    metadata(original_ms)
