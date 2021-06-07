"""Automaticaly generate artifact getters."""
import logging
from typing import Any, Callable, Optional

from metaflow import Run
from toolz import compose_left, identity

from flowrider.client.cache import cache_getter_fn
from flowrider.utils import flow_name_from_path, load_run_id, run_id_path

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
