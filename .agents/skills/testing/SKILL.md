---
name: testing
description: Run the project's verification (`./check`) and auto-fix (`./fix`) pipelines, and diagnose verification failures.
compatibility: requires poetry, python >= 3.12, shellcheck
license: MIT
---

# Testing

Use this skill when running the GitEx test suite, validating new changes before committing, or diagnosing CI failures.

Two root-level scripts wrap the verification pipelines: `./check` for running the full suite of static and runtime tests, and `./fix` for auto-fixing what can be reliable auto-fixed. Prefer calling these scripts over invoking the underlying tools directly.

Do NOT use this skill for authoring tests or scripts. See the [shell-scripts](../shell-scripts/SKILL.md) and [python-tests](../python-tests/SKILL.md) skills for those.

## Rules

-   **Verify.**

    Run `./check` from the repo root. It executes, in order:

    1. ShellCheck on `bin/*` and `lib/*` (`--severity=style`).
    2. Ruff lint on `test/`.
    3. pytest on `test/` (verbose).

    A non-zero exit at any stage fails the run.

    _*Always run `./check` before pushing.*

-   **Auto-fix.**

    Run `./fix` before committing Python changes. It currently runs Ruff format on `test/`.

    There is no autofixer for shell. ShellCheck findings must be addressed by hand.

-   **Set up.**

    `poetry install` MUST have run at least once, and again after any change to `pyproject.toml` or `poetry.lock`.

    The devcontainer runs this automatically as its `postCreateCommand`.

-   **Diagnose.**

    If a verification stage fails, drill into the per-domain skill:

    - ShellCheck failures: see [the shell-scripts skill](../shell-scripts/SKILL.md).

    - Ruff / pytest failures: see [the python-tests skills](../python-tests/SKILL.md).

-   **Commit message validation.**

    This is not part of `/check`. It runs only in CI via the `commit-validation.yaml` GitHub workflow.

    See [the commit skill](https://raw.githubusercontent.com/kieranpotts/skills/refs/heads/dev/skills/utils/git/commits/SKILL.md).

## Examples

Before pushing a branch:

```sh
./check && git push
```

Lint a single script without running the full pipeline:

```sh
shellcheck --severity=style bin/git-foo
```
