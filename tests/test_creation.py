import os
import re
from contextlib import contextmanager
from subprocess import check_output

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
        p = check_output(args).decode("ascii").strip()
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
        p = check_output(args).decode("ascii").strip()
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
        p = check_output(args).decode("ascii").strip()
        if pytest.param.get("openess") == "private":
            assert p == "proprietary"
        else:
            assert p == "MIT"

    def test_makefile(self):
        """Test Makefile exists with no curlies."""
        makefile_path = self.path / "Makefile"
        assert makefile_path.exists()
        assert no_curlies(makefile_path)

    def test_folders(self):
        """Test folders we expect to exist, actually exist."""
        repo_name = pytest.param.get("repo_name")
        expected_dirs = [
            "",
            ".git",
            ".github",
            "bin",
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
            f"{repo_name}/config/pipeline",
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

        assert len(set(abs_expected_dirs) ^ set(abs_dirs)) == 0

    @pytest.mark.usefixtures("conda_env")
    def test_conda(self):
        """Test conda environment is created."""
        repo_name = pytest.param.get("repo_name")

        with ch_dir(self.path):
            p = check_output(["make", "conda-create"]).decode("ascii").strip()
            assert (
                p.splitlines()[-1] == f"Created environment {repo_name}"
            ), "Could not make Conda env"
            assert self.env_path.exists()

            # Add an extra pip dependency
            check_output(["echo", "nuts_finder", ">>", "requirements.txt"])
            p = check_output(["make", "conda-update"]).decode("ascii").strip()

            # Add an extra conda dependency
            check_output(["echo", "  - tqdm", ">>", "environment.yaml"])
            p = check_output(["make", "conda-update"]).decode("ascii").strip()

    def test_git(self):
        """Test expected git branches exist."""
        with ch_dir(self.path):
            p = set(
                (
                    line.strip()
                    for line in check_output(["git", "branch"])
                    .decode("ascii")
                    .strip()
                    .splitlines()
                )
            )
            # Expect to differ by one as either main/master will exist
            assert len(p ^ {"* 0_setup_cookiecutter", "dev", "main", "master"}) == 1

    @pytest.mark.usefixtures("conda_env")
    def test_all(self):
        """Test `make test-setup` command."""
        with ch_dir(self.path):
            p = (
                check_output(["make", "test-setup", "IN_PYTEST=true"])
                .decode("ascii")
                .strip()
                .splitlines()
            )
            assert "In test-suite: Skipping S3 checks" in p
            assert "In test-suite: Skipping Github checks" in p
