"""Tests for UV_INDEX failsafe guidance in templates and docs."""

from pathlib import Path

REPO_ROOT = Path(__file__).parents[1]
TEMPLATE_ENVRC = REPO_ROOT / "{{ cookiecutter.module_name }}" / ".envrc"
TEMPLATE_README = REPO_ROOT / "{{ cookiecutter.module_name }}" / "README.md"
STRUCTURE_DOC = REPO_ROOT / "docs" / "structure.md"


def test_template_envrc_includes_uv_index_failsafe_comment() -> None:
    text = TEMPLATE_ENVRC.read_text()
    assert "# unset UV_INDEX" in text
    assert "private UV_INDEX" in text


def test_template_readme_includes_uv_index_rollback_steps() -> None:
    text = TEMPLATE_README.read_text()
    assert "unset UV_INDEX" in text
    assert "uv sync --no-cache --upgrade" in text
    assert "uv lock --no-cache --upgrade" in text


def test_structure_docs_include_uv_index_failsafe_steps() -> None:
    text = STRUCTURE_DOC.read_text()
    assert "unset UV_INDEX" in text
    assert "uv sync --no-cache --upgrade" in text
    assert "uv lock --no-cache --upgrade" in text
