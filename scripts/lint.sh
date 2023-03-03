#!/usr/bin/env bash

set -e
set -x

mypy infisicalpy
ruff check infisicalpy tests
black infisicalpy tests --check
isort infisicalpy tests --check-only
