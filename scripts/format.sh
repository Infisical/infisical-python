#!/bin/sh -e
set -x

ruff check infisicalpy tests --fix
black infisicalpy tests
isort infisicalpy tests
