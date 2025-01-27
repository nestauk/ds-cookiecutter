import shutil
from pathlib import Path
from subprocess import check_output

import pytest
from cookiecutter import main

CCDS_ROOT = Path(__file__).parents[1].resolve()

base_args = {
    "project_name": "NestaTestCookie".lower(),
    "author_name": "Nesta",
    "repo_name": "nestatestcookie",
    "openness": "public",
}
test_params = [
    {**base_args, "venv_type": venv_type} for venv_type in ["uv", "venv", "conda"]
]


def get_test_id(test_param: dict) -> str:
    assert "venv_type" in test_param
    return test_param["venv_type"]


@pytest.fixture(scope="class", params=test_params, ids=get_test_id)
def default_baked_project(tmpdir_factory, request):
    temp = tmpdir_factory.mktemp("data-project")
    out_dir = Path(temp).resolve()

    pytest.param = request.param
    main.cookiecutter(
        str(CCDS_ROOT), no_input=True, extra_context=pytest.param, output_dir=out_dir
    )

    project_name = pytest.param.get("project_name") or "project_name"
    project_path = out_dir / project_name
    request.cls.path = project_path

    # Set up env_dir for tests
    venv_type = pytest.param["venv_type"]
    if venv_type == "conda":
        repo_name = pytest.param["repo_name"]
        env_dir = (
            Path(check_output(["conda", "info", "--base"]).decode().strip())
            / "envs"
            / repo_name
        )
    else:  # venv
        env_dir = project_path / ".venv"
    request.cls.env_path = env_dir

    yield

    env_dir.exists() and shutil.rmtree(env_dir)
    shutil.rmtree(out_dir)
