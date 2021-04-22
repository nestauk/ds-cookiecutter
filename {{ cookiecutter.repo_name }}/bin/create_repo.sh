#!/bin/bash
set -euo pipefail

source "$PWD/.env.shared"

DESCRIPTION=$(pip show $PROJECT_NAME | grep Summary | cut -d " " -f2-)

# Create
gh repo create nestauk/$PROJECT_NAME --$PROJECT_OPENNESS -d "$DESCRIPTION" -y
# Set default branch to `dev`
gh api -X PATCH -F default_branch=dev repos/nestauk/$PROJECT_NAME
