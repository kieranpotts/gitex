# GitEx

## Project overview

GitEx is a suite of Git extensions implemented as POSIX-compliant Unix shell scripts. Each script integrates with Git as an alias, providing shortcuts for common operations like `git sync`, `git amend`, and `git squash`.

Inspired by (but not compatible with) Git Extras. Some operations are potentially destructive and may rewrite commit history.

## Tech stack

- POSIX shell scripts (`bin/`, `lib/`).
- Python 3.12+ with Poetry 2.2+ for the test suite (`test/`).
- ShellCheck for shell linting; Ruff for Python linting and formatting.
- Markdown for user and developer documentation (`docs/`).

## Repository structure

- `bin/` – The executable `git-<name>` scripts. Any file here that is on the user's `PATH` is auto-discovered by Git as a `git <name>` subcommand. No registration is needed – the user just needs to drop these files into their `PATH` to enable each Git alias.

- `lib/` – Shared shell components sourced by `bin/` scripts (`print.sh` for messaging helpers, `ansi-codes.sh` for color variables).

- `docs/` – Markdown documentation, including per-command usage docs (`docs/usage/git-<name>.md`) and developer-facing docs for setup, testing, and configuration.

- `test/` – The pytest suite. Tests invoke `bin/` scripts as subprocesses against throwaway Git repositories, so all tests are effectively integration-level.

- `skills/` – On-demand context for agents (see the *Skills* section below).

- `check`, `fix` – Root-level dev-tool scripts (see *Dev tools* below).

## Tools

There is nothing to build - `bin/` scripts ship as source, installed by putting `bin/` on the user's `PATH`.

- `./check` – Runs the full verification pipeline: ShellCheck on `bin/` and `lib/`, Ruff lint on `test/`, then pytest. Must pass before pushing.

- `./fix` – Runs automated fixers (currently Ruff format on `test/`). There is no autofixer for shell. ShellCheck findings must be addressed manually.

- `poetry install` – One-time setup of the Python test dependencies, repeated after any change to `pyproject.toml` or `poetry.lock`. The devcontainer runs this automatically.

## Rules

The capitalized words REQUIRED, MUST, MUST NOT, RECOMMENDED, SHOULD, SHOULD NOT, OPTIONAL, and MAY, in the context of this document and agent skills/instructions/rules, are to be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

- The trunk branch is `dev`, not `main`. Open PRs against `dev`.

- All written content (code comments, docs, commit messages) is in American English, with full sentences terminated by periods.

- All shell scripts MUST run under Bash, Zsh, and Dash, and also Git-Bash-for-Windows and WSL2.

- Do not introduce dependencies that would break POSIX compatibility. No Bashisms.

## Skills

- `./skills/testing/SKILL.md`: Instructions for running static and runtime tests (`./check`) and automated fixes (`./fix`).

- `./skills/shell-scripts/SKILL.md`: Coding conventions and design patterns for the shell scripts in `bin/` and `lib/`.

- `./skills/python-tests/SKILL.md`: Coding conventions and design patterns for the pytest suite in `test/`.

- `./skills/documentation/SKILL.md`: Formatting conventions for the Markdown docs in `docs/`.

- `./skills/new-command/SKILL.md`: End-to-end checklist for adding a new `git-<name>` extension (script, test, usage doc, indexes).

- `https://github.com/kieranpotts/skills/blob/dev/skills/utils/git/commits/SKILL.md`: Commit message format enforced by CI, and the semantics of each allowed type.
