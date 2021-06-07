import importlib
import logging
from pathlib import Path
from typing import Any, Dict, List


import yaml
from toolz import get_in, valmap


class HookError(Exception):
    pass


def load_hook(name):
    module_str, method_str = name.rsplit(".", 1)
    try:
        module = importlib.import_module(module_str)
        return getattr(module, method_str)
    except (AttributeError, ModuleNotFoundError) as e:
        raise HookError(*e.args)


def parse_config(path: Path) -> Dict[str, Any]:

    raw_config = yaml.safe_load(path.open())

    def _run_hooks(v):
        if isinstance(v, dict) and "hook" in v:
            hook = load_hook(get_in(["hook", "name"], v))
            args = get_in(["hook", "args"], v, [])
            kwargs = get_in(["hook", "kwargs"], v, {})
            logging.debug(hook, args, kwargs)
            return hook(*args, **kwargs)  # TODO: TypeError: missing args
        else:
            return v

    try:
        config = {k: valmap(_run_hooks, v) for k, v in raw_config.items()}
        logging.debug(f"Parsed config: {config}")
    except HookError as e:
        e.args = (*e.args, f"in file: {str(path)}")
        raise

    return config


def merge_package_suffixes(config: dict, suffixes: List[str]) -> dict:
    """Merge any existing package-suffixes with the minimum required for bundling."""
    if "package-suffixes" not in config["preflow_kwargs"]:
        config["preflow_kwargs"]["package-suffixes"] = ",".join(suffixes)
    elif isinstance(config["preflow_kwargs"]["package-suffixes"], str):
        config["preflow_kwargs"]["package-suffixes"] += ",".join(suffixes)
    elif isinstance(config["preflow_kwargs"]["package-suffixes"], list):
        config["preflow_kwargs"]["package-suffixes"] = ",".join(
            set(config["preflow_kwargs"]["package-suffixes"] + suffixes)
        )
    else:
        TypeError(
            "Expected config['preflow_kwargs']['package-suffixes'] to be str of List[str]"
        )

    return config
