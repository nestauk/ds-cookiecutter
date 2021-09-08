#!/bin/bash

function get_metaflow_config() {
    set -euo pipefail

    PROJECT_DIR="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../..")"

    # Fetch research daps key
    aws s3 cp s3://nesta-production-config/research_daps.key .

    # Clone research daps
    cd /tmp
    \rm -rf /tmp/research_daps
    git clone git@github.com:nestauk/research_daps.git
    cd research_daps

    # Unencrypt research daps
    git-crypt unlock "$PROJECT_DIR/research_daps.key" &> /dev/null

    # Copy metaflow config
    mkdir -p "$HOME/.metaflowconfig"
    cp research_daps/config/metaflowconfig/config.json "$HOME/.metaflowconfig/config_ds-cookiecutter.json"

    # Clean up
    \rm -rf /tmp/research_daps
    cd "$PROJECT_DIR"
    rm research_daps.key
}
