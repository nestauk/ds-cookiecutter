from typing import List

from metaflow import namespace
from pydantic import BaseModel, StrictStr

from flowrider.client import auto_getter

namespace("{{ cookiecutter.repo_name }}")


class Context(BaseModel):
    ds_type: str


class Data(BaseModel):
    column1: List[StrictStr]


def get_context() -> Context:
    """Lots of nice documentation detailing the artifact here..."""
    path, tag, artifact = "example/example_flow", "local", "info"
    data = Context(**auto_getter(path, tag, artifact, local=True))
    return data


def get_data() -> Context:
    """Lots of nice documentation detailing the artifact here..."""
    path, tag, artifact = "example/example_flow", "local", "data"
    data = Data.parse_obj(auto_getter(path, tag, artifact, local=True))
    return data


if __name__ == "__main__":
    print(get_context())
    print(get_data())
