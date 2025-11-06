# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GitEx is a suite of Git extensions implemented as POSIX-compliant Unix shell scripts. These extensions integrate with Git as aliases and provide convenient shortcuts for common Git operations like `git sync`, `git amend`, `git squash`, etc.

The project is inspired by (but not compatible with) Git Extras. Some operations are potentially destructive and may rewrite commit history.

## Architecture

### Core Components

- **bin/**: Contains ~60 Git extension scripts (e.g., `git-whoami`, `git-amend`, `git-sync`). Each script follows POSIX shell compliance and has a standard structure:
  - Shebang: `#!/bin/env sh`
  - Error handling: `set -eu`
  - Header comment with description, usage, and dependencies
  - `main()` function containing implementation
  - Call to `main` at the end

- **lib/**: Shared library code
  - `ansi-codes.sh`: ANSI color code definitions for terminal output formatting (exports variables like `$RED`, `$BOLD`, `$RESET`)

- **test/**: Python-based test suite using pytest
  - `conftest.py`: Pytest configuration with `temp_repo` fixture
  - `helper.py`: Contains `TempRepo` class for creating isolated temporary Git repositories using GitPython
  - `test_*.py`: Test files matching each Git extension (e.g., `test_git_whoami.py`)

- **docs/**: AsciiDoc documentation
  - `requirements.adoc`, `installation.adoc`: Setup instructions
  - `usage/*.adoc`: Individual command documentation
  - `runtime-tests.adoc`, `static-analysis.adoc`: Development process documentation

## Development Commands

### Running Tests

Tests use pytest with GitPython to create isolated temporary repositories. Tests do not modify global or user-level Git configuration.

```bash
# Install dependencies (requires Python >= 3.12, Poetry >= 2.2)
poetry install

# Run all tests
poetry run pytest

# Run tests with verbose output
poetry run pytest -v

# Run a specific test file
poetry run pytest test/test_git_whoami.py

# Run a specific test function
poetry run pytest test/test_git_whoami.py::TestGitWhoami::test_with_name_and_email_set
```

### Static Analysis

ShellCheck is used for shell script linting:

```bash
# Install ShellCheck (Debian-based systems)
sudo apt-get install -y shellcheck

# Lint all shell scripts (only errors, not warnings)
shellcheck --severity=error bin/* lib/*
```

Ruff is used for Python linting and formatting:

```bash
# Lint Python code
poetry run ruff check test/

# Format Python code (run before committing)
poetry run ruff format test/
```

## Development Guidelines

### Shell Scripts (bin/ and lib/)

- Must be POSIX-compliant (works in Bash, Zsh, Dash, etc.)
- Use `set -eu` for error handling
- Follow the standard script structure (see bin/git-whoami for reference)
- Include header comments with description, usage, and dependencies
- Wrap implementation in a `main()` function
- Must pass ShellCheck with `--severity=error`

### Python Tests (test/)

- Use the `temp_repo` fixture from conftest.py for test isolation
- Import `TempRepo` from helper.py if additional repository setup is needed
- Follow existing test patterns (see test/test_git_whoami.py)
- Tests must not modify global Git configuration
- Run Ruff formatter before committing

### Documentation

- User-facing docs are in AsciiDoc format (.adoc)
- Each Git extension has a corresponding doc in docs/usage/
- Link syntax: `link:./path/file.adoc[Display Text]`

## CI/CD

GitHub Actions workflows (in .github/workflows/):

- **integration.yaml**: Runs on push/PR to dev branch
  - Lint job: ShellCheck + Ruff
  - Test job: Poetry + pytest

- **commit-validation.yaml**: Validates commit messages

The main branch for this repository is `dev` (not `main` or `master`).

## Key Constraints

- All shell scripts must remain POSIX-compliant (no Bash-specific features)
- The project structure mirrors Git's extension mechanism: scripts named `git-<command>` in PATH become `git <command>` aliases
- Windows compatibility requires Git Bash or WSL2
