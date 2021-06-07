import os
import re
from pathlib import Path
from typing import Optional


def _repo_name_fallback() -> Optional[str]:
    """Read `REPO_NAME` from `.env.shared`.

    WHY? have to do it this hacky way to keep within stdlib+metaflow during bundling
    """
    content = (Path(__file__).parents[1] / ".env.shared").open().read()
    groups = re.findall(r"REPO_NAME=(.*?)\n", content)
    return groups[0] if groups else None


REPO_NAME = os.getenv("REPO_NAME") or _repo_name_fallback()
if not REPO_NAME:
    raise ValueError("Require `REPO_NAME` environment variable")

SRC_DIR = Path(__file__).parents[1].resolve() / REPO_NAME

__all__ = ["SRC_DIR", "REPO_NAME"]
