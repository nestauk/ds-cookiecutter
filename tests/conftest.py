import shutil
from pathlib import Path
from subprocess import check_output

import pytest
from cookiecutter import main

CCDS_ROOT = Path(__file__).parents[1].resolve()

base_args = {
    "project_name": "Nesta Test Cookie",
    "module_name": "nestatestcookie",
    "openness": "public",
    "python_version": "3.13",
    "autosetup": "yes",
}
test_params = [
    {**base_args, "venv_type": venv_type, "file_structure": file_structure}
    for venv_type in ["uv", "venv", "conda"]
    for file_structure in ["simple", "standard", "full"]
]


def get_test_id(test_param: dict) -> str:
    assert "venv_type" in test_param and "file_structure" in test_param
    return f"{test_param['venv_type']}-{test_param['file_structure']}"


@pytest.fixture(scope="class", params=test_params, ids=get_test_id)
def default_baked_project(tmpdir_factory: pytest.TempdirFactory, request: pytest.FixtureRequest):  # noqa: ANN201
    temp = tmpdir_factory.mktemp("data-project")
    out_dir = Path(temp).resolve()

    pytest.param = request.param
    main.cookiecutter(str(CCDS_ROOT), no_input=True, extra_context=pytest.param, output_dir=out_dir)

    module_name = pytest.param["module_name"]
    project_path = out_dir / module_name
    request.cls.path = project_path

    # Set up env_dir for tests
    if pytest.param["venv_type"] == "conda":
        env_dir = Path(check_output(["conda", "info", "--base"]).decode().strip()) / "envs" / module_name
    else:  # venv
        env_dir = project_path / ".venv"
    request.cls.env_path = env_dir

    yield

    env_dir.exists() and shutil.rmtree(env_dir)
    shutil.rmtree(out_dir)
