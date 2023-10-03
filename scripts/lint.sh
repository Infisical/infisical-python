#!/usr/bin/env bash

set -e
set -x

mypy infisical
ruff check infisical tests
black infisical tests --check
