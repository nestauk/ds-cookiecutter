import shutil
from pathlib import Path
from subprocess import check_output

import pytest
from cookiecutter import main

CCDS_ROOT = Path(__file__).parents[1].resolve()

args = {
    "project_name": "NestaTestCookie".lower(),
    "author_name": "Nesta",
    "repo_name": "nestatestcookie",
}


@pytest.fixture(scope="class", params=[args])
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
    yield

    # cleanup after
    shutil.rmtree(out_dir)


@pytest.fixture(scope="class", params=[args])
def conda_env(request):
    pytest.param = request.param

    repo_name = pytest.param.get("repo_name")

    env_dir = (
        Path(check_output(["conda", "info", "--base"]).decode().strip())
        / "envs"
        / repo_name
    )

    request.cls.env_path = env_dir
    yield

    shutil.rmtree(env_dir)
