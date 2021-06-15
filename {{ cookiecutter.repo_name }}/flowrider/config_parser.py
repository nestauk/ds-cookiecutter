import importlib
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from toolz import get_in, valmap


@dataclass
class Config:
    preflow_kwargs: Dict[str, Any]
    flow_kwargs: Dict[str, Any]
    tags: Optional[List[str]]


class HookError(Exception):
    pass


def load_hook(name):
    module_str, method_str = name.rsplit(".", 1)
    try:
        module = importlib.import_module(module_str)
        return getattr(module, method_str)
    except (AttributeError, ModuleNotFoundError) as e:
        raise HookError(*e.args)


def parse_config(path: Path) -> Config:

    raw_config = yaml.safe_load(path.open())

    def _run_hooks(v):
        if isinstance(v, dict) and "hook" in v:
            hook = load_hook(get_in(["hook", "name"], v))
            args = get_in(["hook", "args"], v, [])
            kwargs = get_in(["hook", "kwargs"], v, {})
            logging.debug(hook, args, kwargs)
            return hook(*args, **kwargs)
        else:
            return v

    try:
        config = {k: valmap(_run_hooks, v) for k, v in raw_config.items()}
        logging.debug(f"Parsed config: {config}")
    except HookError as e:
        e.args = (*e.args, f"in file: {str(path)}")
        raise

    return config
