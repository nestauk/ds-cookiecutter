"""Cache."""
import logging
import os
import pickle
from functools import wraps
from pathlib import Path
from tempfile import gettempdir
from typing import Any, Callable

from dotenv import find_dotenv, load_dotenv

# from flowrider import SRC_DIR

logger = logging.getLogger(__file__)

__all__ = ["cache_getter_fn"]


def cache_getter_fn(
    auto_getter: Callable[[str, int, str], Any]
) -> Callable[..., Callable[[str, int, str], Any]]:
    """Cache `flowrider.client.getter.auto_getter` output as pickle.

    If FLOWRIDER_TEMP_DIR env variable is set, this will be used as the cache
     base, otherwise the system default will be used.
    """

    @wraps(auto_getter)
    def inner(flow_name, run_id, artifact, **kwargs):
        cache_path = _get_temp_dir() / auto_getter.__module__ / flow_name / str(run_id)
        cache_filepath = cache_path / artifact

        if not cache_path.exists():
            logger.info(f"Creating cache directory: {cache_path}")
            os.makedirs(cache_path, exist_ok=True)

        if cache_filepath.exists():
            logger.info(f"Loading from cache: {cache_filepath}")
            with open(cache_filepath, "rb") as fp:
                return pickle.load(fp)
        else:
            out = auto_getter(flow_name, run_id, artifact, **kwargs)
            logger.info(f"Caching: {cache_filepath}")
            with open(cache_filepath, "wb") as fp:
                pickle.dump(out, fp)
            return out

    return inner


def _get_temp_dir() -> Path:
    """Use `FLOWRIDER_TEMP_DIR` env var as tempdir or system default if not set."""
    load_dotenv(find_dotenv())
    tempdir = os.getenv("FLOWRIDER_TEMP_DIR") or gettempdir()
    return Path(tempdir).resolve()
