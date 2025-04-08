import os
import re
import shutil
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from subprocess import CalledProcessError, check_output
from typing import List

import pytest
import tomli


@contextmanager
def ch_dir(path):
    """Context Manager to change directory to `path`."""
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield os.getcwd()
    finally:
        os.chdir(cwd)


def no_curlies(filepath):
    """Utility to make sure no curly braces appear in a file.

    That is, was jinja able to render everthing?
    """
    with open(filepath, "r") as f:
        data = f.read()

    template_strings = ["{{", "}}", "{%", "%}"]

    template_strings_in_file = [s in data for s in template_strings]
    return not any(template_strings_in_file)


@pytest.mark.usefixtures("default_baked_project")
class TestCookieSetup(object):
    def test_project_name(self):
        """Test project name matches base path."""
        project = self.path
        name = "NestaTestCookie".lower()
        assert project.name == name

    def test_readme(self):
        """Test README.md exists with no curlies."""
        readme_path = self.path / "README.md"
        assert readme_path.exists()
        assert no_curlies(readme_path)
        with open(readme_path) as fin:
            assert "# NestaTestCookie".lower() == next(fin).strip()

    def test_license(self):
        """Test LICENSE exists with no curlies."""
        license_path = self.path / "LICENSE"
        assert license_path.exists()
        assert no_curlies(license_path)

    def test_metadata(self):
        """Test project metadata in pyproject.toml."""
        pyproject_path = self.path / "pyproject.toml"
        assert pyproject_path.exists()
        assert no_curlies(pyproject_path)

        with open(pyproject_path, "rb") as f:
            pyproject = tomli.load(f)

        project = pyproject.get("project", {})
        assert project.get("name") == "nestatestcookie"
        assert project.get("version") == "0.1.0"
        assert any(
            author.get("name") == "Nesta" for author in project.get("authors", [])
        )
        if pytest.param.get("openness") == "private":
            assert project.get("license", {}).get("text") == "proprietary"
        else:
            assert project.get("license", {}).get("text") == "MIT"

    def test_curlies(self):
        """Test miscellaneous files for no curlies."""
        repo_name = pytest.param.get("repo_name")
        path_stubs = [
            ".env",
            ".envrc",
            "README.md",
            "pyproject.toml",
            "docs/conf.py",
            "docs/index.rst",
            f"{repo_name}/config/logging.yaml",
            f"{repo_name}/__init__.py",
        ]

        assert all((no_curlies(self.path / path_stub) for path_stub in path_stubs))

    def test_folders(self):
        """Test folders we expect to exist, actually exist."""
        repo_name = pytest.param.get("repo_name")
        expected_dirs = [
            "",
            ".git",
            ".github",
            ".cookiecutter",
            ".cookiecutter/state",
            ".recipes",
            "docs",
            "inputs",
            "inputs/data",
            "outputs",
            "outputs/data",
            "outputs/.cache",
            "outputs/figures",
            "outputs/figures/vegalite",
            "outputs/models",
            "outputs/reports",
            repo_name,
            f"{repo_name}/analysis",
            f"{repo_name}/config",
            f"{repo_name}/getters",
            f"{repo_name}/notebooks",
            f"{repo_name}/pipeline",
            f"{repo_name}/utils",
        ]

        abs_expected_dirs = [str(self.path / d) for d in expected_dirs]

        abs_dirs, _, _ = zip(*os.walk(self.path))
        abs_dirs = list(
            filter(
                lambda dir: not any(
                    (
                        re.match(f".*{stub}", dir)
                        for stub in [
                            ".git/",
                            ".vscode",
                            ".pytest_cache",
                            ".ruff_cache",
                            "build",
                            ".egg-info",
                        ]
                    )
                ),
                abs_dirs,
            )
        )

        print(set(abs_expected_dirs) ^ set(abs_dirs))
        assert len(set(abs_expected_dirs) ^ set(abs_dirs)) == 0

    def test_git(self):
        """Test expected git branches exist."""
        with ch_dir(self.path):
            p = set(shell(["git", "branch"]))
            # Expect only main and dev branches to exist
            assert p == {"* dev", "main"}

    def test_env_yaml(self):
        """Test environment.yaml exists if using conda and vice-versa."""
        env_yaml_path = self.path / "environment.yaml"
        uses_conda = pytest.param["venv_type"] == "conda"
        has_env_yaml = env_yaml_path.exists()
        assert uses_conda == has_env_yaml


def shell(cmd: List[str]) -> List[str]:
    """Run `cmd`, checking output and returning stripped output lines."""
    try:
        p = [line.strip() for line in check_output(cmd).decode().strip().splitlines()]
    except CalledProcessError as e:
        for line in (e.stdout or b"").decode().splitlines():
            print(line)
        for line in (e.stderr or b"").decode().splitlines():
            print(line, file=sys.stderr)
        raise e
    return p
