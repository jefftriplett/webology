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

@docs:
    uv run rich-codex --no-confirm --skip-git-checks

@fmt:
    just --fmt --unstable

@lint:
    uv run ruff check .
    uv run ruff format --check .

@lock:
    uv lock

# bump the CalVer version, relock, and push the tag; CI publishes to PyPI
release *ARGS:
    #!/usr/bin/env bash
    set -euo pipefail
    just bump {{ ARGS }}
    just lock
    version="$(grep -m1 '^current_version' pyproject.toml | cut -d'"' -f2)"
    git add uv.lock
    git commit --amend --no-edit
    git tag -d "$version"
    git tag -a "$version" -m "$version"
    git push --follow-tags

@test *ARGS:
    uv run pytest {{ ARGS }}

@update:
    uv run cog -P -r README.md
