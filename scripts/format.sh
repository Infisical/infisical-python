#!/bin/sh -e
set -x

ruff check infisical tests --fix
black infisical tests
