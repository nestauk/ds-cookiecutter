#!/bin/bash

conda_activate() {
    set -euo pipefail

    # Avoid unbound variable error
    export PS1=${PS1:-}

    # shellcheck disable=SC1091
    source "$(conda info --base)/etc/profile.d/conda.sh"  \
    && conda activate "$1"
}
