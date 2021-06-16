#!/bin/bash
set -euo pipefail

# # shellcheck source=./conda_activate.sh
# source "$(dirname "$0")/conda_activate.sh"

# Fetch description of package (setup.py and conda make this horrible)
DESCRIPTION=$(python "$(dirname "$0")/../setup.py" --description)

# Create
gh repo create "$GITHUB_ACCOUNT/$PROJECT_NAME" --"$PROJECT_OPENNESS" -d "$DESCRIPTION" -y

# push initial branches
git push --all

# Set:
# - default branch to `dev`
# - squash merge as only option
gh api --silent -X PATCH \
-F default_branch=dev \
-F allow_merge_commit=false \
-F allow_rebase_merge=false \
"repos/$GITHUB_ACCOUNT/$PROJECT_NAME"
