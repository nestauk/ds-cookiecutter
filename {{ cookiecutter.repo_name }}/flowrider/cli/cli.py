#!/bin/env python
import logging

import typer

from flowrider.cli.runner import run_flow_from_config

app = typer.Typer()

flow_subpath_help = """
Path stub to flow

E.g. `example/flow` will run `pipeline/example/flow.py` using config from
`config/pipeline/example/flow_{TAG}.yaml`.
"""

tag_help = """
Configuration tag to use.

E.g. `production` will use the config from `config/pipeline/{FLOW_SUBPATH}_production.yaml`.

"""


@app.command()
def run(
    flow_subpath: str = typer.Argument(..., help=flow_subpath_help),  # noqa: B008
    tag: str = typer.Option("dev", help=tag_help),  # noqa: B008
):
    """Run and bundle a metaflow using YAML based configuration.

    Writes successfull runs to `config/pipeline/{FLOW_SUBPATH}_{TAG}.run_id`
    """

    typer.secho(f"Running {flow_subpath} with tag {tag} ", fg="black", bg="yellow")
    logging.getLogger().setLevel(logging.INFO)
    run_flow_from_config(flow_subpath, tag)
