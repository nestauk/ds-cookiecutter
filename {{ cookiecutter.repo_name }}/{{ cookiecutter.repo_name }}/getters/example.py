from typing import List

from metaflow import namespace
from pydantic import BaseModel, StrictStr

from flowrider.client import auto_getter
import {{ cookiecutter.repo_name }}
from {{ cookiecutter.repo_name }}.pipeline.example.example_flow import EnvironmentFlow

namespace("{{ cookiecutter.repo_name }}")
MODULE = {{ cookiecutter.repo_name }}


class Context(BaseModel):
    ds_type: str


class Data(BaseModel):
    column1: List[StrictStr]


def get_context() -> Context:
    """Lots of nice documentation detailing the artifact here..."""
    flow, artifact = EnvironmentFlow, "info"
    config_path = "config/pipeline/example/example_flow_local.yaml"
    data = Context(**auto_getter(flow, config_path, artifact, MODULE))
    return data


def get_data() -> Context:
    """Lots of nice documentation detailing the artifact here..."""
    flow, artifact = EnvironmentFlow, "data"
    config_subpath = "config/pipeline/example/example_flow_local.yaml"
    data = Data.parse_obj(auto_getter(flow, config_subpath, artifact, MODULE))
    return data


if __name__ == "__main__":
    # Don't actually run getters as scripts
    print(get_context())
    print(get_data())
