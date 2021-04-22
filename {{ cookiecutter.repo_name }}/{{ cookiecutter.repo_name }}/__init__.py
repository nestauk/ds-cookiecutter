"""{{ cookiecutter.repo_name }}."""
import logging
import logging.config
from pathlib import Path
from typing import Optional

import yaml


def get_yaml_config(file_path: Path) -> Optional[dict]:
    """Fetch yaml config and return as dict if it exists."""
    if file_path.exists():
        with open(file_path, "rt") as f:
            return yaml.load(f.read(), Loader=yaml.FullLoader)


# Define project base directory
project_dir = Path(__file__).resolve().parents[1]


# Read log config file
_log_config_path = Path("config/logging.yaml")
_logging_config = get_yaml_config(_log_config_path)
if _logging_config:
    logging.config.dictConfig(_logging_config)

# Define module logger
logger = logging.getLogger(__name__)

# Model config
_model_config_path = Path("config/logging.yaml")
config = get_yaml_config(_model_config_path)
