import json
import logging
import sys

import metaflow as mf

from flowrider.decorators import son_of_a_batch


def deployment_info(context):
    print(context)
    return json.dumps({"ds_type": context.ds_type})


@son_of_a_batch
@mf.conda_base(libraries={})
class EnvironmentFlow(mf.FlowSpec):
    info = mf.Parameter("deployment_info", type=mf.JSONType, default=deployment_info)

    from flowrider.decorators import pip

    # @mf.conda(libraries={"s3fs": ">0"})
    @pip(libraries={"tqdm": None})
    @mf.step
    def start(self):
        import project_name

        print(project_name.PROJECT_DIR)
        print(project_name.config)

        self.next(self.end)

    @mf.step
    def end(self):
        print(sys.executable)
        print(f"execution context is {self.info}")
        print(mf.metaflow_environment.platform.platform())


def hook():
    print("HOOK RAN")
    return {"ds_type": "hook context"}


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    EnvironmentFlow()
