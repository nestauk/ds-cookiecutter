import logging
import logging.config
import yaml
from pathlib import Path
from typing import Optional


def get_log_config(file_path: Path) -> Optional[dict]:
    if file_path.exists():
        with open(file_path, "rt") as f:
            return yaml.load(f.read(), Loader=yaml.FullLoader)


# Define project base directory
project_dir = Path(__file__).resolve().parents[1]

# Define log output locations
info_out = str(project_dir / "info.log")
error_out = str(project_dir / "errors.log")

# Read log config file
log_config_file = project_dir / "logging.yaml"
logging_config = get_log_config(log_config_file)
if logging_config:
    logging.config.dictConfig(logging_config)

# Define module logger
logger = logging.getLogger(__name__)

# Model config
with open(project_dir / "{{ cookiecutter.repo_name }}" / "model_config.yaml", "rt") as f:
    config = yaml.safe_load(f.read())
