"""Cache."""
import logging
import os
import pickle
from pathlib import Path
from typing import Any, Callable

from dotenv import find_dotenv, load_dotenv

from flowrider import SRC_DIR

logger = logging.getLogger(__file__)

__all__ = ["cache_getter_fn"]


def cache_getter_fn(
    f: Callable[[str, int, str], Any]
) -> Callable[..., Callable[[str, int, str], Any]]:
    """Cache `f` output as pickle if `temp_dir` env var is set."""

    def inner(*args, **kwargs):
        temp_dir = _get_temp_dir()
        to_cache = True if temp_dir and f.__module__ != "__main__" else False

        if not to_cache:
            return f(*args, **kwargs)

        flow_name, run_id, artifact = args
        cache_file = artifact
        cache_path = Path(temp_dir).resolve() / f.__module__ / flow_name / str(run_id)
        cache_filepath = cache_path / cache_file

        if to_cache and not cache_path.exists():
            logger.info(f"Creating cache directory: {cache_path}")
            os.makedirs(cache_path, exist_ok=True)

        if cache_filepath.exists():
            logger.info(f"Loading from cache: {cache_filepath}")
            with open(cache_filepath, "rb") as fp:
                return pickle.load(fp)
        else:
            logger.info(f"Caching: {cache_filepath}")
            out = f(*args, **kwargs)
            with open(cache_filepath, "wb") as fp:
                pickle.dump(out, fp)
            return out

    return inner


def _get_temp_dir() -> str:
    """Find `temp_dir` env var or return None."""
    load_dotenv(find_dotenv())
    try:
        return os.environ["temp_dir"]
    except KeyError:
        return Path(SRC_DIR).parent / "outputs" / ".cache"
