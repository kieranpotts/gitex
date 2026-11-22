# GitEx

GitEx is a suite of Git extensions implemented as POSIX-compliant Unix shell
scripts. Each script integrates with Git as an alias, providing shortcuts for
common operations like `git sync`, `git amend`, and `git squash`.

Inspired by (but not compatible with) Git Extras. Some operations are
potentially destructive and may rewrite commit history.

The capitalized words REQUIRED, MUST, MUST NOT, RECOMMENDED, SHOULD,
SHOULD NOT, OPTIONAL, and MAY are to be interpreted as described in
[IETF RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

## Tech stack

- POSIX shell scripts (`bin/`, `lib/`).

- Python 3.12 with Poetry 2.5 for the test suite (`test/`).

- ShellCheck for shell linting. Ruff for Python linting and formatting.

- mise to pin the versions of Python, Poetry, and ShellCheck, for the host,
  the dev container, and CI (`mise.toml`).

- Markdown for user and developer documentation (`docs/`).

## Project structure

- `bin/`. \
  The executable `git-<name>` scripts. Any file here that is on the user's
  `PATH` is auto-discovered by Git as a `git <name>` subcommand. No
  registration is needed. The user just needs to drop these files into
  their `PATH` to enable each Git alias.

- `lib/`. \
  Shared shell components sourced by `bin/` scripts (`print.sh` for messaging
  helpers, `ansi-codes.sh` for color variables).

- `docs/`. \
  Markdown documentation, including per-command usage docs
  (`docs/usage/git-<name>.md`) and developer-facing docs for setup,
  testing, and configuration.

- `test/`. \
  The pytest suite. Tests invoke `bin/` scripts as subprocesses against
  throwaway Git repositories, so all tests are effectively integration-level.

- `.agents/skills/`. \
  On-demand context for agents (see the *Skills* section below).

- `check`, `fix`. \
  Root-level dev-tool scripts (see *Dev tools* below).

## Tools

There is nothing to build - `bin/` scripts ship as source, installed by
putting `bin/` on the user's `PATH`.

- `./run/check`. \
  Runs the full verification pipeline: ShellCheck on `bin/` and `lib/`, Ruff
  lint on `test/`, then pytest. Must pass before pushing.

- `./fix`. \
  Runs automated fixers (currently Ruff format on `test/`). There is no
  autofixer for shell. ShellCheck findings must be addressed manually.

- `./run/install`. \
  One-time setup of the pinned toolchain (`mise trust`, `mise install`) and
  the Python test dependencies (`poetry install`), repeated after any change to
  `mise.toml`, `pyproject.toml`, or `poetry.lock`. Run it by hand, in the
  workspace devcontainer too, which installs no repository's dependencies.

## Rules

- The trunk branch is `dev`, not `main`. Open PRs against `dev`.

- All written content (code comments, docs, commit messages) is in
  American English, with full sentences terminated by periods.

- All shell scripts MUST run under Bash, Zsh, and Dash, and also
  Git-Bash-for-Windows and WSL2.

- Do not introduce dependencies that would break POSIX compatibility.
  No bashisms.

## Skills

The [`.agents/skills/`](./.agents/skills/) directory provides on-demand skills
for managing this repository. See the [`README`](./.agents/skills/README.md) in
that directory for the full index.

`.claude/skills` is a symlink to `.agents/skills` for auto-discovery by Claude
Code.

- `./.agents/skills/new-gitex-command/SKILL.md`. \
  End-to-end checklist for adding a new `git-<name>` extension
  (script, test, usage doc, indexes). Its `references/` directory holds the
  conventions for the shell scripts, the pytest suite, running checks, and the
  user documentation.
