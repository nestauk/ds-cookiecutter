#!/usr/bin/env bash
set -e


# Configure git hook
chmod +x .githooks/pre-commit
ln -s $PWD/.githooks/pre-commit .git/hooks/pre-commit
