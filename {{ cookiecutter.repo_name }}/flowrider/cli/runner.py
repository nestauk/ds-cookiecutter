"""Utils to execute a metaflow w/ subprocess & update config w/ successful run ID's."""
import json
import logging
import os
import shutil
from itertools import chain, repeat
from pathlib import Path
from shlex import quote
from subprocess import CalledProcessError, run
from typing import Any, Dict, Iterable, List, Optional

import toolz as t

from flowrider.config_parser import Config, parse_config, run_hooks


__all__ = ["run_flow_from_config"]


def run_flow_from_config(
    flow_path: Path,
    config_path: Path,
    project_dir: Path,
    config_extras: Dict[str, Any],
) -> None:
    """Run flow parameterised by YAML config file.

    Args: TODO

    Raises: CalledProcessError
    """

    # Parse and enrich config
    extra_tags: List[str] = t.get("tags", config_extras, [])
    extra_suffixes: List[str] = t.get("package-suffixes", config_extras, [])
    config: Config = t.thread_first(
        config_path,
        parse_config,
        run_hooks,
        (_add_run_id, config_path),
        (_merge_package_suffixes, extra_suffixes),
        (_merge_tags, extra_tags),
    )
    logging.info(f"CONFIG: {config}")

    # If local metadata requested use `.metaflow` in `project_dir`
    if config["preflow_kwargs"].get("metadata") == "local":
        os.environ["METAFLOW_DATASTORE_SYSROOT_LOCAL"] = str(project_dir)

    # Copy flow to base of project - allows bootstrapping with `flowrider.flow.decorators`
    tmp_flow_path = (project_dir / flow_path.name).with_suffix(".py")
    shutil.copy(flow_path, tmp_flow_path)

    try:
        execute_flow(tmp_flow_path, **config)
    except CalledProcessError as exc:
        raise exc
    finally:
        tmp_flow_path.unlink()


def execute_flow(
    flow_path: Path, preflow_kwargs: dict, flow_kwargs: dict, tags: List[str]
):
    """Execute flow in `flow_file` with `params`.

    Args:
        flow_file: File containing metaflow
        params: Keys are flow parameter names, values are parameter values (as strings).
        metaflow_args: Keys are metaflow parameter names passed before run,
            values are parameter values (as strings).

    Returns:
        run_id of flow

    Raises:
        CalledProcessError: When flow execution fails
    """
    cmd = " ".join(
        [
            "python",
            str(flow_path),
            "--no-pylint",
            *_parse_options(preflow_kwargs),
            "run",
            *_parse_options(flow_kwargs),
            *chain.from_iterable(zip(repeat("--tag"), map(quote, tags))),
        ]
    )
    logging.info(f"RUNNING: { cmd }")

    run(cmd, shell=True, check=True)


def _serialise(x: Any) -> str:
    """Serialise `x` to `str` falling back on JSON."""
    if isinstance(x, str):
        return x
    if isinstance(x, Path):
        return str(x)
    else:
        return json.dumps(x)


def _parse_options(options: Dict[str, Any]) -> Iterable[str]:
    """Parse and quote `options` to be passed to metaflow.

    `{"foo": {"data": [1.2, 3, "4"]}} => '--foo', '\'{"data": [1.2, 3, "4"]}\''`
    """
    return t.thread_last(
        options,
        (t.itemmap, lambda item: (f"--{item[0]}", _serialise(item[1]))),
        lambda x: x.items(),
        chain.from_iterable,
        (map, quote),
    )


def _merge_tags(config: Config, extra_tags: List[str]) -> Config:
    """Mix tags from config["tags"] config["flow_kwargs"]["tag"] and extra_tags."""

    extra_tags = list(
        t.cons(t.get_in(["flow_kwargs", "tag"], config, None), extra_tags)
    )
    out = t.update_in(
        config,
        ["tags"],
        lambda current: current + extra_tags,
        [],
    )
    out["flow_kwargs"].pop("tag")  # Placed into top-level "tags" key
    return out


def _add_run_id(config: Config, config_path: Path) -> Config:
    """Ensure a run-id is output alongside `config_path`."""
    return t.assoc_in(
        config, ["flow_kwargs", "run-id-file"], config_path.with_suffix(".run_id")
    )


def _merge_package_suffixes(
    config: Config, suffixes: Optional[List[str]] = None
) -> Config:
    """Merge any existing package-suffixes with the minimum required for bundling."""
    if not isinstance(suffixes, list):
        TypeError(
            "Expected config['preflow_kwargs']['package-suffixes'] to be `List[str]`"
        )

    suffixes = suffixes or []

    keys = ["preflow_kwargs", "package-suffixes"]
    return t.update_in(
        config, keys, lambda current: ",".join([current, *suffixes]).strip(","), ""
    )
