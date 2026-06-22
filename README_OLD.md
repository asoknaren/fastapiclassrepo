# fastapiclassrepo

This project uses [uv](https://docs.astral.sh/uv/) for Python dependency and environment management.

## Quick start

1. Sync the environment:

   uv sync

2. Activate the virtual environment (PowerShell):

   .\.venv\Scripts\Activate.ps1

## Dependency management

- Add a runtime dependency:

  uv add <package>

- Add a development dependency:

  uv add --dev <package>

- Remove a dependency:

  uv remove <package>

- Recreate lockfile after edits:

  uv lock

## Run commands in project environment

Use `uv run` to execute commands using the project environment without manually activating it.

Examples:

- uv run python --version
- uv run pytest
