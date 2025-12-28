# Please see: https://github.com/jefftriplett/scripts-to-rule-them-all

set dotenv-load := false

@_default:
    just --list

@bootstrap:
    uv sync

@build:
    uv build

@bump *ARGS:
    uv run bumpver update {{ ARGS }}

@bump-dry:
    just bump --dry

@check:
    uv run twine check dist/*

@docs:
    uv run rich-codex --no-confirm --skip-git-checks

@fmt:
    just --fmt --unstable

@lint:
    uv run black --check .
    uv run flake8

@test:
    uv run pytest

@update:
    uv run cog -P -r README.md

@upload:
    uv run twine upload dist/*
