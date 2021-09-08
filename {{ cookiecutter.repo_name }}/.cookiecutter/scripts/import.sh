#!/bin/bash
set -euo pipefail

# Import bash functions from files
for filename in "create_bucket.sh" "create_repo.sh" "install_metaflow_aws.sh" "conda_activate.sh";
do
    # shellcheck disable=SC1090
    source "$(dirname "${BASH_SOURCE[0]}")/$filename";
done;
