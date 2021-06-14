import json
import logging
import sys

import metaflow as mf

from flowrider.flow.decorators import son_of_a_batch


def deployment_info(context):
    print(context)
    return json.dumps({"ds_type": context.ds_type})


# @son_of_a_batch  # works as a class / step decorator - step is more efficient
class EnvironmentFlow(mf.FlowSpec):
    info = mf.Parameter("deployment_info", type=mf.JSONType, default=deployment_info)

    from flowrider.flow.decorators import pip

    # @mf.conda(libraries={"s3fs": ">0"})
    @son_of_a_batch
    @pip(libraries={"tqdm": None})
    @mf.step
    def start(self):
        import {{ cookiecutter.repo_name }}

        print({{ cookiecutter.repo_name }}.PROJECT_DIR)
        print({{ cookiecutter.repo_name }}.config)

        import pandas as pd

        self.data = pd.DataFrame({"column1": range(10)}, dtype=str).to_dict("list")

        self.next(self.end)

    @mf.step
    def end(self):
        print(sys.executable)
        print(f"execution context is {self.info}")
        print(mf.metaflow_environment.platform.platform())


def hook(a, b):
    print("HOOK RAN with:", a, b)
    return {"ds_type": "hook context"}


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    EnvironmentFlow()
