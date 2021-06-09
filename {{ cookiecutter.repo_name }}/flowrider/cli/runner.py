"""Utils to execute a metaflow w/ subprocess & update config w/ successful run ID's."""
import importlib
import json
import logging
import os
import shutil
import tempfile
from itertools import chain, repeat
from pathlib import Path
from shlex import quote
from subprocess import CalledProcessError, run
from typing import Any, Dict, Iterable, List

import toolz.curried as t

from flowrider.cli.bundle import bundle
from flowrider.config_parser import merge_package_suffixes, parse_config


SUFFIXES = [
    ".py",  # Source files
    ".yaml",  # Config
    ".md",  # setup.py reads README.md
    ".txt",  # E.g. requirements.txt
    ".env.shared",  # Gets cookiecutter metadata
]


__all__ = ["run_flow_from_config"]


def run_flow_from_config(flow_subpath: str, tag: str, pkg_name: str) -> int:
    """Run flow parameterised by YAML config file.

    Runs flow in `{pkg_name}.pipeline.{flow_subpath}` with config
    from `config/pipeline/{flow_subpath}_{tag}.yaml` within the folder 
    that `pkg_name` is located.

    Args:
        flow_subpath:
        tag:
        src_dir: Package source path

    Returns:
        Metaflow run ID
    """

    src_dir = Path(importlib.import_module(pkg_name).__file__).parent

    # Base project path
    project_dir = src_dir.parent

    # Path to flow
    flow_path = (src_dir / "pipeline" / flow_subpath).with_suffix(".py")
    assert flow_path.exists()
    # Path to flow config
    config_path = (
        src_dir / "config" / "pipeline" / f"{flow_subpath}_{tag}"
    ).with_suffix(".yaml")
    assert config_path.exists()

    # Parse config and add run id param
    config = parse_config(config_path)

    # Enrich config
    # TODO add these as some form of middleware?
    config["flow_kwargs"]["run-id-file"] = config_path.with_suffix(".run_id")
    config = merge_package_suffixes(config, SUFFIXES)
    config["tags"] = t.pipe(
        config.get("tags", []) + [config["flow_kwargs"].pop("tag", ""), src_dir.name],
        t.filter(None),
        list,
    )
    logging.info(f"CONFIG: {config}")

    # Put local metadata in project
    metadata = config["preflow_kwargs"].get("metadata")
    if metadata == "local":
        os.environ["METAFLOW_DATASTORE_SYSROOT_LOCAL"] = str(project_dir)

    # Copy flow temporarily to base of project? Would there be conflicts if files are changed?
    # TODO add temp suffix?
    tmp_flow_path = (project_dir / flow_path.name).with_suffix(".py")
    shutil.copy(flow_path, tmp_flow_path)

    run_id = execute_flow(tmp_flow_path, **config)

    tmp_flow_path.unlink()

    return run_id


def execute_flow(
    flow_path: Path, preflow_kwargs: dict, flow_kwargs: dict, tags: List[str]
) -> int:
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

    try:
        run(cmd, shell=True, check=True)
    except CalledProcessError as exc:
        raise exc

    with open(flow_kwargs["run-id-file"], "r") as f:
        run_id = int(f.read())
    return run_id


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
