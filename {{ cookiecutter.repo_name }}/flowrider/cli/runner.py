"""Utils to execute a metaflow w/ subprocess & update config w/ successful run ID's."""
import importlib
import json
import logging
import os
import shutil
from functools import partial
from itertools import chain, repeat
from pathlib import Path
from shlex import quote
from subprocess import CalledProcessError, run
from typing import Any, Dict, Iterable, List

import toolz.curried as t

from flowrider.config_parser import Config, parse_config


SUFFIXES = ",".join(
    [
        ".py",  # Source files
        ".yaml",  # Config
        ".md",  # setup.py reads README.md
        ".txt",  # E.g. requirements.txt
        ".env.shared",  # Gets cookiecutter metadata
    ]
)


__all__ = ["run_flow_from_config"]


def run_flow_from_config(flow_subpath: str, tag: str, pkg_name: str) -> int:
    """Run flow parameterised by YAML config file.

    Runs flow in `{pkg_name}.pipeline.{flow_subpath}` with config
    from `config/pipeline/{flow_subpath}_{tag}.yaml` within the folder
    that `pkg_name` is located.

    Args:
        flow_subpath:
        tag:
        pkg_name:

    Returns:
        Metaflow run ID
    """
    src_dir = Path(importlib.import_module(pkg_name).__file__).parent
    project_dir = src_dir.parent

    # Path to flow
    flow_path = (src_dir / "pipeline" / flow_subpath).with_suffix(".py")
    if not flow_path.exists():
        raise FileNotFoundError(flow_path)

    # Path to flow config
    config_path = (
        src_dir / "config" / "pipeline" / f"{flow_subpath}_{tag}"
    ).with_suffix(".yaml")
    if not config_path.exists():
        raise FileNotFoundError(config_path)

    # Parse and enrich config
    config = t.pipe(
        config_path,
        parse_config,
        partial(_add_run_id, config_path=config_path),
        partial(_merge_package_suffixes, suffixes=SUFFIXES),
        partial(_merge_tags, extra_tags=[src_dir.name]),
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
    return t.pipe(
        options,
        t.itemmap(lambda item: (f"--{item[0]}", _serialise(item[1]))),
        lambda x: x.items(),
        chain.from_iterable,
        t.map(quote),
    )


def _merge_tags(config: Config, extra_tags: List[str]) -> Config:
    """Mix tags from config["tags"] config["flow_kwargs"]["tag"] and extra_tags."""
    tags = t.pipe(
        config.get("tags", []) + [config["flow_kwargs"].pop("tag", ""), *extra_tags],
        t.filter(None),
        list,
    )
    return t.assoc(config, "tags", tags)


def _add_run_id(config: Config, config_path: Path) -> Config:
    """Ensure a run-id is output alongside `config_path`."""
    return t.assoc_in(
        config, ["flow_kwargs", "run-id-file"], config_path.with_suffix(".run_id")
    )


def _merge_package_suffixes(config: Config, suffixes: str) -> Config:
    """Merge any existing package-suffixes with the minimum required for bundling."""
    if not isinstance(suffixes, str):
        TypeError("Expected config['preflow_kwargs']['package-suffixes'] to be `str`")

    keys = ["preflow_kwargs", "package-suffixes"]
    return t.assoc_in(config, keys, t.get(config, keys, "") + suffixes)
