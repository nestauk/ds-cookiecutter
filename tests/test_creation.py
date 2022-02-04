import os
import re
import sys
from contextlib import contextmanager
from glob import glob
from pathlib import Path
from subprocess import CalledProcessError, check_output
from typing import List

import pytest


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

    def test_author(self):
        """Test author set in `setup.py`."""
        setup_ = self.path / "setup.py"
        args = ["python", setup_, "--author"]
        p = "".join(shell(args))
        assert p == "Nesta"

    def test_readme(self):
        """Test README.md exists with no curlies."""
        readme_path = self.path / "README.md"
        assert readme_path.exists()
        assert no_curlies(readme_path)
        with open(readme_path) as fin:
            assert "# NestaTestCookie".lower() == next(fin).strip()

    def test_version(self):
        """Test version set in `setup.py`."""
        setup_ = self.path / "setup.py"
        args = ["python", setup_, "--version"]
        p = "".join(shell(args))
        assert p == "0.1.0"

    def test_license(self):
        """Test LICENSE exists with no curlies."""
        license_path = self.path / "LICENSE"
        assert license_path.exists()
        assert no_curlies(license_path)

    def test_license_type(self):
        """Test License set appropriately in `setup.py`."""
        setup_ = self.path / "setup.py"
        args = ["python", setup_, "--license"]
        p = "".join(shell(args))
        if pytest.param.get("openess") == "private":
            assert p == "proprietary"
        else:
            assert p == "MIT"

    def test_makefile(self):
        """Test Makefile exists with no curlies."""
        makefile_path = self.path / "Makefile"
        assert makefile_path.exists()
        assert no_curlies(makefile_path)

    def test_curlies(self):
        """Test miscellaneous files for no curlies."""
        repo_name = pytest.param.get("repo_name")
        path_stubs = [
            ".env",
            ".envrc",
            "README.md",
            "setup.cfg",
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
            ".cookiecutter/scripts",
            "inputs",
            "outputs",
            repo_name,
            f"{repo_name}/analysis",
            f"{repo_name}/config",
            f"{repo_name}/getters",
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
                        for stub in [".git/", ".vscode", ".pytest_cache"]
                    )
                ),
                abs_dirs,
            )
        )

        print(set(abs_expected_dirs) ^ set(abs_dirs))
        assert len(set(abs_expected_dirs) ^ set(abs_dirs)) == 0

    @pytest.mark.usefixtures("conda_env")
    def test_conda(self):
        """Test conda environment is created."""

        with ch_dir(self.path):
            try:
                p = shell(["make", ".cookiecutter/state/conda-create"])
                assert " DONE" in p[-1]
                assert self.env_path.exists()

                # Add an extra pip dependency
                check_output(["echo", "nuts_finder", ">>", "requirements.txt"])
                p = shell(["make", "conda-update"])

                # Add an extra conda dependency
                check_output(["echo", "  - tqdm", ">>", "environment.yaml"])
                p = shell(["make", "conda-update"])
            except CalledProcessError:
                log_path = Path(".cookiecutter/state/conda-create.log")
                if log_path.exists():
                    with log_path.open() as f:
                        print("conda-create.log:\n", f.read())
                raise

    def test_git(self):
        """Test expected git branches exist."""
        with ch_dir(self.path):
            p = set(shell(["git", "branch"]))
            # Expect to differ by one as either main/master will exist
            assert len(p ^ {"* 0_setup_cookiecutter", "dev", "main", "master"}) == 1

    @pytest.mark.usefixtures("conda_env")
    def test_all(self):
        """Test `make test-setup` command."""
        with ch_dir(self.path):
            try:
                shell(["make", "install"])
                p = shell(["make", "test-setup", "IN_PYTEST=true"])
                assert "In test-suite: Skipping S3 checks" in p
                assert "In test-suite: Skipping Github checks" in p
                assert all(("ERROR:" not in line for line in p))
            except CalledProcessError:
                for log_path in glob(".cookiecutter/state/*.log"):
                    with open(log_path) as f:
                        print(f"{log_path}:\n", f.read())
                raise
            except AssertionError:
                print(p)


def shell(cmd: List[str]) -> List[str]:
    """Run `cmd`, checking output and returning stripped output lines."""
    try:
        p = [line.strip() for line in check_output(cmd).decode().strip().splitlines()]
    except CalledProcessError as e:
        [print(line) for line in (e.stdout or b"").decode().splitlines()]
        [
            print(line, file=sys.stderr)
            for line in (e.stderr or b"").decode().splitlines()
        ]
        raise e
    return p
