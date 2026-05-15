---
name: new-command
description: End-to-end checklist for adding a new git-<name> extension - script, test, usage doc, indexes.
compatibility: requires sh, poetry, python >= 3.12, shellcheck, pytest
license: MIT
---

# New command

Use this skill when implementing one of the unchecked entries in [`TODO.md`](../../TODO.md), or otherwise adding a new `git-<name>` extension.

A command is not complete until four artifacts and three indexes have all landed. Skipping any one will fail `./check`, fail CI, or leave the project visibly inconsistent.

Do NOT use this skill for modifying an existing command (use the relevant per-domain skill directly) or for renaming/removing commands (the steps differ).

## Instructions

For a new command `git <name>` (e.g., `git foo`, or `git push-all` for a multi-word command):

1. **Script.** Create `bin/git-<name>` and `chmod +x` it. Follow [`../shell-scripts/SKILL.md`](../shell-scripts/SKILL.md). Templates:
   - [`bin/git-whoami`](../../bin/git-whoami): no-options commands.
   - [`bin/gitex`](../../bin/gitex): commands with a small fixed flag set.
   - [`bin/git-author`](../../bin/git-author): full option parsing.

2. **Test.** Create `test/test_git_<name>.py`. Follow [`../python-tests/SKILL.md`](../python-tests/SKILL.md), using [`test/test_git_whoami.py`](../../test/test_git_whoami.py) as the canonical example. Cover at minimum: happy path, one error path, argument validation.

   The filename mapping is load-bearing: `test_git_push_all.py` resolves to `bin/git-push-all` via the `bin` fixture (each `_` becomes `-`). A mismatched name silently fails to resolve the script.

3. **Usage doc.** Verify or create `docs/usage/git-<name>.adoc`. Follow [`../documentation/SKILL.md`](../documentation/SKILL.md). Usage docs are often stubbed upfront to drive the design - when implementing, verify the implementation matches the stub rather than rewriting it.

4. **Validate.** Run [`./check`](../../check) (see [`../testing/SKILL.md`](../testing/SKILL.md)). All three stages - ShellCheck, Ruff, pytest - must pass before commit.

5. **Sync the three indexes:**
   - [`TODO.md`](../../TODO.md): flip `[ ]` to `[x]`.
   - [`bin/gitex`](../../bin/gitex): add a one-line entry under `_print_commands()` matching the alphabetical order and two-space indent of existing entries.
   - [`README.adoc`](../../README.adoc) and [`docs/usage/README.adoc`](../../docs/usage/README.adoc): both list every command. Entries usually already exist because the usage doc was stubbed first; verify rather than blindly add.

6. **Commit.** A new command is conventionally `feature: …`. See [`../commits/SKILL.md`](../commits/SKILL.md).

## Examples

A complete change set for `git foo`:

```
bin/git-foo                       (new, executable)
test/test_git_foo.py              (new)
docs/usage/git-foo.adoc           (verified or created)
bin/gitex                         (one-line addition under _print_commands)
TODO.md                           ([ ] -> [x])
README.adoc                       (verify entry exists)
docs/usage/README.adoc            (verify entry exists)
```

Commit message:

```
feature: add git foo
```

## Rules

- **Multi-word commands.** Use kebab-case in the script name (`bin/git-push-all`) and snake_case in the test name (`test/test_git_push_all.py`). Underscores in test filenames map to hyphens in script names - never the reverse.
- **Stub usage doc already exists.** Don't rewrite from scratch. The stub encodes the intended CLI surface. If implementation diverges, decide which is right and update only what needs to change.
- **`bin/gitex --commands` is hand-maintained.** Forgetting to add a line is silent - there's no test enforcing parity between `bin/` and `_print_commands()`. Double-check.

## References

- [`../shell-scripts/SKILL.md`](../shell-scripts/SKILL.md), [`../python-tests/SKILL.md`](../python-tests/SKILL.md), [`../documentation/SKILL.md`](../documentation/SKILL.md): per-artifact conventions.
- [`../testing/SKILL.md`](../testing/SKILL.md): running the validation pipeline.
- [`../commits/SKILL.md`](../commits/SKILL.md): commit-message format.
- [`TODO.md`](../../TODO.md): current implementation status of all planned commands.
