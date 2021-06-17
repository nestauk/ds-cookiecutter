#!/bin/bash

function create_gh_repo() {
    set -euo pipefail

    GITHUB_ACCOUNT=$1
    REPO_NAME=$2
    PROJECT_OPENNESS=$3

    # Fetch description of package (setup.py and conda make this horrible)
    DESCRIPTION=$(python "$(dirname "${BASH_SOURCE[0]}")/../../setup.py" --description)

    gh repo create "$GITHUB_ACCOUNT/$REPO_NAME" --"$PROJECT_OPENNESS" -d "$DESCRIPTION" -y

    # push initial branches
    git push --all

    # Set:
    # - default branch to `dev`
    # - squash merge as only option
    gh api -X PATCH \
    -F default_branch=dev \
    -F allow_merge_commit=false \
    -F allow_rebase_merge=false \
    "repos/$GITHUB_ACCOUNT/$REPO_NAME"
}