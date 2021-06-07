#!/bin/env python
import typer

from flowrider.metaflow_runner import run_flow_from_config

app = typer.Typer()


@app.command()
def run(
    path: str = typer.Argument(..., help="path docs"),  # noqa: B008
    tag: str = typer.Option("dev", help="tag docs"),  # noqa: B008
):
    """Runs `flows/$PATH.py` using configuration from `config/flows/$PATH_$TAG.yaml`."""

    typer.secho(f"Running {path} with tag {tag} ", fg="black", bg="yellow")
    run_flow_from_config(path, tag)


if __name__ == "__main__":
    app()
