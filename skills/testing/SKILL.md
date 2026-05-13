---
name: testing
description: Run the project's verification (./check) and auto-fix (./fix) pipelines, or diagnose a failure in either.
compatibility: requires poetry, python >= 3.12, shellcheck
license: MIT
---

# Testing

Use this skill when running the gitex test suite, validating a branch before pushing, or diagnosing CI failures. Two root-level scripts wrap the pipelines; prefer them over invoking the underlying tools directly so the full suite stays consistent.

Do NOT use this skill for authoring tests or scripts. See the `shell-scripts`, `python-tests`, and `commits` skills for those.

## Instructions

1. **Verify.** Run `./check` from the repo root. It executes, in order:
   1. ShellCheck on `bin/*` and `lib/*` (`--severity=style`).
   2. Ruff lint on `test/`.
   3. pytest on `test/` (verbose).

   A non-zero exit at any stage fails the run. **Always run `./check` before pushing.**

2. **Auto-fix.** Run `./fix` before committing Python changes. It currently runs Ruff format on `test/`. There is no autofixer for shell. ShellCheck findings must be addressed by hand.

3. **Set up.** `poetry install` must have run at least once, and again after any change to `pyproject.toml` or `poetry.lock`. The devcontainer runs this automatically as its `postCreateCommand`.

4. **Diagnose.** If a stage fails, drill into the per-domain skill:
   - ShellCheck failures: see [`../shell-scripts/SKILL.md`](../shell-scripts/SKILL.md).
   - Ruff / pytest failures: see [`../python-tests/SKILL.md`](../python-tests/SKILL.md).

## Examples

Before pushing a branch:

```sh
./check && git push
```

Lint a single script without running the full pipeline:

```sh
shellcheck --severity=style bin/git-foo
```

## Edge cases

- The `check` and `fix` scripts themselves are shell scripts but are not scanned by ShellCheck. Scope is `bin/*` and `lib/*` only.
- Commit message validation is NOT part of `./check`. It runs only in CI via the `commit-validation.yaml` workflow. See [`../commits/SKILL.md`](../commits/SKILL.md).
- Anything outside `bin/`, `lib/`, and `test/` (e.g., `docs/`, `.devcontainer/`, `.github/`) is not covered.

## References

- [`../shell-scripts/SKILL.md`](../shell-scripts/SKILL.md): ShellCheck scope and shell conventions.
- [`../python-tests/SKILL.md`](../python-tests/SKILL.md): Ruff and pytest details.
- [`../commits/SKILL.md`](../commits/SKILL.md): commit-message validation pipeline.
- [`../../docs/runtime-tests.adoc`](../../docs/runtime-tests.adoc), [`../../docs/static-analysis.adoc`](../../docs/static-analysis.adoc): end-user docs for the same pipelines.
