"""Utils to execute a metaflow w/ subprocess & update config w/ successful run ID's."""
import json
import logging
import os
from itertools import chain
from pathlib import Path
from shlex import quote
from subprocess import CalledProcessError, run
from typing import Any, Dict, Iterable

import toolz.curried as t

from flowrider import SRC_DIR
from flowrider.bundle import bundle
from flowrider.config_parser import merge_package_suffixes, parse_config


SUFFIXES = [
    ".py",  # Source files
    ".yaml",  # Config
    ".md",  # setup.py reads README.md
    ".txt",  # E.g. requirements.txt
    ".env.shared",  # Gets cookiecutter metadata
]


__all__ = ["run_flow_from_config"]


def run_flow_from_config(flow_subpath: str, tag: str, src_dir: Path = SRC_DIR) -> int:
    """Run flow parameterised by YAML config file.

    Runs flow at `{SRC_DIR}/pipeline/{flow_subpath}.py` with config
    from `{SRC_DIR}/config/pipeline/{flow_subpath}_{tag}.yaml`.

    Args:
        flow_subpath:
        tag:
        src_dir: Package source path

    Returns:
        Metaflow run ID
    """

    # Base project path
    project_dir = src_dir.parent

    # Path to flow
    flow_path = (src_dir / "pipeline" / flow_subpath).with_suffix(".py")
    # Path to flow config
    config_path = (
        src_dir / "config" / "pipeline" / f"{flow_subpath}_{tag}"
    ).with_suffix(".yaml")

    # Parse config and add run id param
    config = parse_config(config_path)
    # TODO add these as some form of middleware?
    config["flow_kwargs"]["run-id-file"] = config_path.with_suffix(".run_id")
    config = merge_package_suffixes(config, SUFFIXES)
    logging.info(f"CONFIG: {config}")

    # Make a copy of the project (Files with `SUFFIXES` only) in a tempdir
    # TODO: bundle + son_of_a_batch points local install to /tmp/... ?
    tmp_path = bundle(
        project_dir,
        flow_path,
        SUFFIXES,
    )
    logging.info(f"BUNDLED: [{project_dir},{flow_path}] -> {tmp_path}")
    os.chdir(tmp_path)  # XXX: Working directory change!

    run_id = execute_flow(Path(flow_path.with_suffix(".py").name), **config)

    return run_id


def execute_flow(flow_path: Path, preflow_kwargs: dict, flow_kwargs: dict) -> int:
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
