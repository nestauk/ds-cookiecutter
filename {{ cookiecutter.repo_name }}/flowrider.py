import importlib
import logging
from pathlib import Path
from typing import Optional

import typer

import flowrider
from flowrider.cli.runner import run_flow_from_config

app = typer.Typer()

flow_subpath_help = """Path stub to flow

E.g. `example/flow` will run `pipeline/example/flow.py` using config from
`config/pipeline/example/flow_{TAG}.yaml`."""

tag_help = """Configuration tag to use.

E.g. `production` will use the config from `config/pipeline/{FLOW_SUBPATH}_production.yaml`."""

pkg_name_help = "Package name of flow"


@app.command()
def run(
    flow_subpath: str = typer.Argument(..., help=flow_subpath_help),  # noqa: B008
    tag: str = typer.Option("dev", help=tag_help),  # noqa: B008
    pkg_name: Optional[str] = typer.Option(None, help=pkg_name_help),  # noqa: B008
):
    """Run and bundle a metaflow using YAML based configuration.

    Writes successfull runs to `config/pipeline/{FLOW_SUBPATH}_{TAG}.run_id`
    """
    logging.getLogger().setLevel(logging.INFO)

    pkg_name = pkg_name or Path(flowrider.__file__).parents[1].name
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

    # Tags and package-suffixes are merged with user YAML config
    config_extras = {
        "tags": [src_dir.name],
        "package-suffixes": [
            ".py",  # Source files
            ".yaml",  # Config
            ".md",  # setup.py reads README.md
            ".txt",  # E.g. requirements.txt
            ".env.shared",  # Gets cookiecutter metadata
            "PKG-INFO",
        ],
    }

    typer.secho(f"Running {flow_subpath} with tag {tag} ", fg="black", bg="yellow")
    run_flow_from_config(flow_path, config_path, project_dir, config_extras)


if __name__ == "__main__":
    app()
