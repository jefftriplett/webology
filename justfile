# Please see: https://github.com/jefftriplett/scripts-to-rule-them-all

set dotenv-load := false

@_default:
    just --list

@bootstrap:
    pip install -U -r requirements.in

@build:
    python -m build

@check:
    twine check dist/*

@fmt:
    just --fmt --unstable

@lint:
    black .
    blacken-docs ./README.md

@test:
    pytest

@update:
    cog -P -r README.md

@upload:
    twine upload dist/*
