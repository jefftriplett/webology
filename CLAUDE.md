# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal "business card" CLI tool that displays Jeff Triplett's contact info and projects in the terminal with animated effects. Run it with `uvx webology`.

## Commands

```bash
# Setup
just bootstrap          # Install dependencies with uv

# Development
just build              # Build the package
just lint               # Run black --check and flake8
just test               # Run pytest
just docs               # Generate docs images with rich-codex

# Version management
just bump               # Bump version (uses bumpver with CalVer YYYY.MM.INC1)
just bump-dry           # Preview version bump

# Publishing
just check              # Check dist with twine
just upload             # Upload to PyPI
```

## Architecture

Single-file application (`webology.py`) using:
- **Rich** for terminal UI (panels, colors, live updates, spinners)
- **Typer** for CLI entry point

Key functions:
- `make_gradient_text()` - Creates rainbow-colored text from a color palette
- `typing_effect()` - Animates text appearing character-by-character with Rich Live
- `main()` - Orchestrates spinner → rainbow header → typing animation

Content is stored in module constants (`ASCII_ART`, `CARD_CONTENT`, `RAINBOW_COLORS`).

## Version Syncing

Version is defined in two places and synced by bumpver:
- `pyproject.toml` (version field)
- `webology.py` (`__version__`)
