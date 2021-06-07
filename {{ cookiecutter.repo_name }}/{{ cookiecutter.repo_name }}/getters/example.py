from pydantic import BaseModel, StrictStr, ValidationError
from metaflow import metadata

from flowrider.client import auto_getter


class Context(BaseModel):
    ds_type: str


def get_example() -> Context:
    """Lots of nice documentation detailing the artifact here..."""
    path, tag, artifact = "example/example_flow", "local", "info"
    return Context(**auto_getter(path, tag, artifact))


if __name__ == "__main__":
    metadata("/tmp")
    print(get_example())

if False:
    # %%
    from typing import List
    import pandas as pd

    class Foo(BaseModel):
        column1: List[StrictStr]

    data = pd.DataFrame({"column1": range(10)}, dtype=str)
    print("Success...", Foo.parse_obj(data.to_dict("list")))

    try:
        data = pd.DataFrame({"column1": range(10)}, dtype=int)
        print(Foo(**data.to_dict("list")))
    except ValidationError:
        print("Bad column type")

    # %%
