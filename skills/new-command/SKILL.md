---
name: new-command
description: End-to-end checklist for adding a new git-<name> extension.
compatibility: requires sh, poetry, python >= 3.12, shellcheck, pytest
license: MIT
---

# New command

Use this skill when implementing one of the unchecked entries in `TODO.md`, or otherwise when adding a new `git-<name>` extension.

A command is not complete until four artifacts and three indexes have all landed. Skipping any one will leave the project in an inconsistent state.

Do NOT use this skill when modifying an existing skill.

## Instructions

Work through these in order for a new command `git <name>` (eg. `git foo`, or `git push-all` for a multi-word command):

1.  **Script.**

    Create `bin/git-<name>` and `chmod +x` it. Follow the [shell-scripts skill](../shell-scripts/SKILL.md).

    Use these as reference implementations:

   - [`bin/git-whoami`](../../bin/git-whoami): For commands with no-options commands.

   - [`bin/gitex`](../../bin/gitex): For commands with a small fixed flag set.

   - [`bin/git-author`](../../bin/git-author): For commands with full option parsing.

2.  **Test.**

    Create `test/test_git_<name>.py`.

    Follow the [python-tests skill](../python-tests/SKILL.md), using [`test/test_git_whoami.py`](../../test/test_git_whoami.py) as the canonical example.

    Cover at minimum: happy path, one error path, argument validation.

    The filename mapping is load-bearing: `test_git_push_all.py` resolves to `bin/git-push-all` via the `bin` fixture (each `_` becomes `-`). A mismatched name silently fails to resolve the script.

3.  **Docs.**

    Verify or create `docs/usage/git-<name>.adoc`. Follow the [documentation skill](../documentation/SKILL.md).

    Usage docs are often stubbed up-front to drive the design. When implementing, verify the implementation matches the stub, rather than rewriting it.

4.  **Validate.**

    Run [`./check`](../../check) – see the [testing skill](../testing/SKILL.md)). All three stages - ShellCheck, Ruff, pytest - MUST pass before commit.

5.  **Sync the command indexes:**

    - [`bin/gitex`](../../bin/gitex): Add a one-line entry under `_print_commands()`, matching the alphabetical order and two-space indent of existing entries.

    - [`docs/usage/README.adoc`](../../docs/usage/README.adoc)

    - [`README.adoc`](../../README.adoc)

    - [`TODO.md`](../../TODO.md): Flip `[ ]` to `[x]`.

6.  **Commit.**

    A new command is conventionally committed as a feature: `feature: …`. See [the commits skill](https://raw.githubusercontent.com/kieranpotts/skills/refs/heads/dev/skills/utils/git/commits/SKILL.md).

## Rules

-   **Multi-word commands.**

    Use kebab-case in the script name (`bin/git-push-all`) and snake_case in the test name (`test/test_git_push_all.py`).

    Underscores in test filenames map to hyphens in script names - never the reverse.

-   **Stub usage doc already exists.**

    Don't rewrite from scratch. The stub encodes the intended CLI surface. If implementation diverges, decide which is right and update only what needs to change.

-  **`bin/gitex --commands` is hand-maintained.**

    Forgetting to add a line is silent - there's no test enforcing parity between `bin/` and `_print_commands()`. Double-check.

## Examples

A complete change set for `git foo`:

```
bin/git-foo              - New executable.
bin/gitex                - One-line addition under _print_commands.
docs/usage/README.adoc   - Updated to reference the new command.
docs/usage/git-foo.adoc  - Created or updated from stub.
test/test_git_foo.py     - New test.
README.adoc              - Updated to reference the new command.
TODO.md                  - `foo` command marked as implemented.
```

Commit message:

```
feature: add `git foo`
```

## References

- [`TODO.md`](../../TODO.md): current implementation status of all planned commands.
