import pytest

from runner import _add_run_id, _merge_package_suffixes, _merge_tags


def test_merge_tags():
    assert _merge_tags({"tags": ["foo"], "flow_kwargs": {"tag": "bar"}}, ["baz"]) == {
        "tags": ["foo", "bar", "baz"],
        "flow_kwargs": {},
    }

    assert _merge_tags({"tags": ["foo"], "flow_kwargs": {"tag": "bar"}}, []) == {
        "tags": ["foo", "bar"],
        "flow_kwargs": {},
    }

    with pytest.raises(TypeError):
        assert _merge_tags({"tags": ["foo"], "flow_kwargs": {"tag": "bar"}}, None)


def test_merge_package_suffixes():
    def construct_config(suffixes):
        return {"preflow_kwargs": {"package-suffixes": suffixes}}

    assert _merge_package_suffixes({}, [".py"]) == construct_config(".py")
    assert _merge_package_suffixes({}, None) == construct_config("")

    assert _merge_package_suffixes({"preflow_kwargs": {}}, [".py"]) == construct_config(
        ".py"
    )
    assert _merge_package_suffixes({"preflow_kwargs": {}}, None) == construct_config("")

    assert _merge_package_suffixes(construct_config(""), [".py"]) == construct_config(
        ".py"
    )
    assert _merge_package_suffixes(construct_config(""), None) == construct_config("")

    assert _merge_package_suffixes(
        construct_config(".yaml"), [".py"]
    ) == construct_config(".yaml,.py")
    assert _merge_package_suffixes(construct_config(".yaml"), None) == construct_config(
        ".yaml"
    )

    # TypeError
    with pytest.raises(TypeError):
        _merge_package_suffixes({"preflow_kwargs": {"package-suffixes": ".yaml"}}, 1)


def test_add_run_id():
    from pathlib import Path

    assert _add_run_id({}, Path("/foo/bar")) == {
        "flow_kwargs": {"run-id-file": Path("/foo/bar.run_id")}
    }
