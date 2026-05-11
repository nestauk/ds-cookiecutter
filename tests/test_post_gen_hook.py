"""Tests for hooks/post_gen_project.sh remote-repo creation behavior."""

import os
import shutil
import stat
import subprocess
from pathlib import Path

import jinja2
import pytest

HOOK_PATH = Path(__file__).parents[1] / "hooks" / "post_gen_project.sh"

BASE_CONTEXT = {
    "repo_name": "testrepo",
    "openness": "public",
    "venv_type": "uv",
    "create_remote": "yes",
}


def _render(context: dict) -> str:
    return jinja2.Template(HOOK_PATH.read_text()).render(cookiecutter=context)


def _write_stub(path: Path, name: str, body: str = "exit 0") -> None:
    stub = path / name
    stub.write_text(
        f'#!/bin/bash\necho "{name} $*" >> "$STUB_LOG"\n{body}\n'
    )
    stub.chmod(stub.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


@pytest.fixture
def stub_env(tmp_path):
    """Build PATH with stub binaries for gh, direnv, and git-push interception."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    log = tmp_path / "stub.log"
    log.touch()

    _write_stub(bin_dir, "gh")
    _write_stub(bin_dir, "direnv")

    # git wrapper: log all calls, short-circuit `push`, delegate everything else
    real_git = shutil.which("git")
    assert real_git, "git must be on PATH to run these tests"
    (bin_dir / "git").write_text(
        f'#!/bin/bash\n'
        f'echo "git $*" >> "$STUB_LOG"\n'
        f'if [ "$1" = "push" ]; then exit 0; fi\n'
        f'exec {real_git} "$@"\n'
    )
    (bin_dir / "git").chmod(0o755)

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"
    env["STUB_LOG"] = str(log)
    # Ensure git commit works in CI without global config
    env["GIT_AUTHOR_NAME"] = "Test"
    env["GIT_AUTHOR_EMAIL"] = "test@example.com"
    env["GIT_COMMITTER_NAME"] = "Test"
    env["GIT_COMMITTER_EMAIL"] = "test@example.com"
    return env, log


def _run_hook(tmp_path: Path, context: dict, env: dict) -> subprocess.CompletedProcess:
    work = tmp_path / "work"
    work.mkdir()
    script = work / "post_gen_project.sh"
    script.write_text(_render(context))
    script.chmod(0o755)
    # Hook expects to optionally remove this file when venv_type != conda
    (work / "environment.yaml").write_text("")
    return subprocess.run(
        ["bash", str(script)],
        cwd=work,
        env=env,
        capture_output=True,
        text=True,
    )


class TestCreateRemoteYes:
    def test_calls_gh_repo_create_under_nestauk(self, tmp_path, stub_env):
        env, log = stub_env
        result = _run_hook(tmp_path, BASE_CONTEXT, env)
        assert result.returncode == 0, result.stderr
        log_text = log.read_text()
        assert "gh auth status" in log_text
        assert (
            "gh repo create nestauk/testrepo --public --source=. --remote=origin"
            in log_text
        )

    def test_pushes_both_branches(self, tmp_path, stub_env):
        env, log = stub_env
        result = _run_hook(tmp_path, BASE_CONTEXT, env)
        assert result.returncode == 0, result.stderr
        log_text = log.read_text()
        assert "git push -u origin main" in log_text
        assert "git push -u origin dev" in log_text

    def test_sets_default_branch_to_dev(self, tmp_path, stub_env):
        env, log = stub_env
        result = _run_hook(tmp_path, BASE_CONTEXT, env)
        assert result.returncode == 0, result.stderr
        assert (
            "gh repo edit nestauk/testrepo --default-branch dev" in log.read_text()
        )

    def test_private_visibility_flag(self, tmp_path, stub_env):
        env, log = stub_env
        ctx = {**BASE_CONTEXT, "openness": "private"}
        result = _run_hook(tmp_path, ctx, env)
        assert result.returncode == 0, result.stderr
        assert "gh repo create nestauk/testrepo --private" in log.read_text()

    def test_fails_when_gh_not_authenticated(self, tmp_path, stub_env):
        env, log = stub_env
        bin_dir = Path(env["PATH"].split(os.pathsep)[0])
        # Replace gh stub so `gh auth status` returns nonzero
        (bin_dir / "gh").write_text(
            '#!/bin/bash\n'
            'echo "gh $*" >> "$STUB_LOG"\n'
            'if [ "$1" = "auth" ] && [ "$2" = "status" ]; then exit 1; fi\n'
            'exit 0\n'
        )
        (bin_dir / "gh").chmod(0o755)
        result = _run_hook(tmp_path, BASE_CONTEXT, env)
        assert result.returncode != 0
        assert "gh not authenticated" in result.stderr
        log_text = log.read_text()
        assert "gh repo create" not in log_text


class TestCreateRemoteNo:
    def test_skips_all_remote_calls(self, tmp_path, stub_env):
        env, log = stub_env
        ctx = {**BASE_CONTEXT, "create_remote": "no"}
        result = _run_hook(tmp_path, ctx, env)
        assert result.returncode == 0, result.stderr
        log_text = log.read_text()
        assert "gh auth status" not in log_text
        assert "gh repo create" not in log_text
        assert "gh repo edit" not in log_text
        assert "git push" not in log_text

    def test_prints_manual_remote_message(self, tmp_path, stub_env):
        env, _ = stub_env
        ctx = {**BASE_CONTEXT, "create_remote": "no"}
        result = _run_hook(tmp_path, ctx, env)
        assert result.returncode == 0, result.stderr
        assert "manually set GitHub remote" in result.stdout
