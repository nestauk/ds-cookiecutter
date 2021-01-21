#!/usr/bin/env bash
set -e

# Configure git hook
chmod +x .githooks/pre-commit
[ -f .git/hooks/pre-commit ] || ln -s $PWD/.githooks/pre-commit .git/hooks/pre-commit
