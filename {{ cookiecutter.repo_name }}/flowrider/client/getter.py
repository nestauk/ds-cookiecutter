"""Automaticaly generate artifact getters.

WARNING: Currently specific to ds-cookiecutter path conventions.
"""
import importlib
import re
from contextlib import contextmanager
from pathlib import Path
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
    tag: str,
    artifact: str,
    cache_strategy: Optional[Callable] = cache_getter_fn,
) -> Any:
    """Return flow object based on `path` and `tag`.

    - Loads `run_id` from `config/pipeline/{path}_{tag}.run_id
    - Introspects name of flow

    Args:
        flow_subpath:
        tag:
        artifact:
        cache_strategy: Decorator to cache artifact with, if `None` no caching.

    Returns:
        Metaflow data artifact
    """
    cache_strategy = cache_strategy or identity

    # E.g. If flow is "project_name.pipeline.example.example_flow.EnvironmentFlow"
    module = flow.__module__
    repo_name = module.split(".")[0]
    flow_subpath = re.findall("pipeline/(.*)", module.replace(".", "/").strip("/"))[0]
    # module -> "project_name.pipeline.example.example_flow.EnvironmentFlow"
    # repo_name -> "project_name"
    # flow_subpath -> "example/example_flow"
    flow_name = flow.__name__
    src_dir = Path(importlib.import_module(repo_name).__file__).parent
    # flow_name -> "EnvironmentFlow"
    # src_dir -> /tmp/project_name

    run_id = load_run_id(_run_id_path(flow_subpath, tag, src_dir))

    @cache_strategy
    def get(flow_name, run_id, artifact):
        return getattr(Run(f"{flow_name}/{run_id}").data, artifact)

    config_path = (
        src_dir / "config" / "pipeline" / f"{flow_subpath}_{tag}"
    ).with_suffix(".yaml")
    config = parse_config(config_path)
    if config["preflow_kwargs"].get("metadata", None) == "local":
        with _metadata(f"local@{src_dir.parent}"):
            return get(flow_name, run_id, artifact)
    else:
        return get(flow_name, run_id, artifact)


@contextmanager
def _metadata(ms):
    """Context manager to use Metaflow local metadata."""
    original_ms = get_metadata()
    metadata(ms)
    yield
    metadata(original_ms)


def _run_id_path(flow_subpath: str, tag: str, src_dir: Path) -> Path:
    """Construct path to run id for flow corresponding to `{path}_{tag}`.

    E.g. "myflow/flow"
    """
    return src_dir / "config" / "pipeline" / f"{flow_subpath}_{tag}.run_id"
