#!/bin/bash
set -euo pipefail

# Avoid unbound variable error
export PS1=${PS1:-}

conda_activate() {
    source "$(conda info --base)/etc/profile.d/conda.sh"  \
    && conda activate "$PROJECT_NAME"
}
