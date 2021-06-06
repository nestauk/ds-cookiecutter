"""Utils to execute a metaflow w/ subprocess & update config w/ successful run ID's."""
import json
import logging
import os
from itertools import chain
from pathlib import Path
from shlex import quote
from subprocess import CalledProcessError, Popen

import toolz.curried as t
from flowrider import SRC_DIR
from flowrider.bundle import bundle
from flowrider.config_parser import parse_config


logger = logging.getLogger(__file__)

# File suffixes to bundle
SUFFIXES = [".py", ".yaml", ".md", ".txt", ".env.shared"]


def _serialise(x):
    return x if isinstance(x, str) else json.dumps(x)


def execute_flow(flow_file: Path, preflow_kwargs: dict, flow_kwargs: dict) -> int:
    """Execute flow in `flow_file` with `params`.

    Args:
        flow_file: File containing metaflow
        params: Keys are flow parameter names (command-line notation,
             `--`), values are parameter values (as strings).
        metaflow_args: Keys are metaflow parameter names passed before run
            (command-line notation, `--`), values are parameter values (as strings).

    Returns:
        run_id of flow

    Raises:
        CalledProcessError: When flow execution fails
    """
    parse = t.compose_left(
        t.itemmap(lambda item: (f"--{item[0]}", _serialise(item[1]))),
        lambda x: x.items(),
        chain.from_iterable,
        t.map(quote),
    )

    # run_id_file = flow_file.parents[0] / ".run_id"
    run_id_file = flow_kwargs["run-id-file"]
    cmd = " ".join(
        [
            "python",
            str(flow_file),
            "--no-pylint",
            *parse(preflow_kwargs),
            "run",
            # "--run-id-file",
            # str(run_id_file),
            # PARAMS
            *parse(flow_kwargs),
        ]
    )
    logger.info(cmd)

    # RUN FLOW
    proc = Popen(
        cmd,
        shell=True,
    )
    while proc.poll():
        print("poll")
        print(proc.communicate())
    proc.wait()
    return_value = proc.returncode

    if return_value != 0:
        raise CalledProcessError(return_value, cmd)
    else:
        with open(run_id_file, "r") as f:
            run_id = int(f.read())
        return run_id


def run_flow_from_config(path: str, tag: str) -> int:
    """Run flow parameterised by YAML config file.

    Runs flow at `{SRC_DIR}/pipeline/{path}.py` with config
    from `{SRC_DIR}/config/pipeline/{path}_{tag}.yaml`.

    Args:
        path:
        tag:

    Returns:
    """

    # Package source path
    src_dir = SRC_DIR
    # Base project path
    project_dir = src_dir.parent

    # Path to flow
    flow_path = (src_dir / "pipeline" / path).with_suffix(".py")
    # Path to flow config
    config_path = (src_dir / "config" / "pipeline" / f"{path}_{tag}").with_suffix(
        ".yaml"
    )

    # Parse config and add run id param
    config = parse_config(config_path)
    config["flow_kwargs"]["run-id-file"] = str(
        config_path.parent / f"{path}_{tag}.run_id"
    )
    config["preflow_kwargs"]["package-suffixes"] = ",".join(SUFFIXES)
    logging.info(config)

    # BUNDLE
    tmp_path = bundle(
        project_dir,
        flow_path,
        SUFFIXES,
    )
    os.chdir(tmp_path)
    logging.info(f"BUNDLED: [{project_dir},{flow_path}] -> {tmp_path}")

    run_id = execute_flow((tmp_path / path).with_suffix(".py"), **config)

    return run_id
