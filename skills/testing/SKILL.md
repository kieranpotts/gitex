# Testing

Two root-level scripts wrap the project's verification and auto-fix pipelines. Prefer them over invoking the underlying tools directly, so that the full suite is exercised consistently.

## `./check` - full verification

Runs every static and runtime check, in this order:

1. **ShellCheck** on `bin/*` and `lib/*` (`--severity=style`).
2. **Ruff lint** on `test/`.
3. **pytest** on `test/` (verbose).

A non-zero exit from any stage fails the whole run.

**Always run `./check` before pushing.**

Requires `poetry install` to have been run at least once, and again after any change to `pyproject.toml` or `poetry.lock`. The devcontainer runs `poetry install` automatically as its `postCreateCommand`, so no manual setup is needed when working in-container.

To drill into a single failing layer, see [`../shell-scripts/SKILL.md`](../shell-scripts/SKILL.md) for ShellCheck details or [`../python-tests/SKILL.md`](../python-tests/SKILL.md) for pytest and Ruff details.

## `./fix` - automated fixes

Runs automated fixers:

1. **Ruff format** on `test/`.

Run `./fix` before committing Python changes. There are no automated fixers for shell scripts - ShellCheck findings must be addressed manually.

## Not covered

- Commit message validation - handled separately by the `commit-validation.yaml` CI workflow. See [`../commits/SKILL.md`](../commits/SKILL.md).
- The `check` and `fix` scripts themselves - they are shell scripts but are not currently scanned by ShellCheck (which only targets `bin/*` and `lib/*`).
- Anything outside `bin/`, `lib/`, and `test/`.
