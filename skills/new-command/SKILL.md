# New command

Use this skill when implementing one of the unchecked entries in [`TODO.md`](../../TODO.md), or otherwise adding a new `git-<name>` extension.

A command is not complete until four artifacts and three indexes have all landed. Skipping any one will fail `./check`, fail CI, or leave the project visibly inconsistent.

## Artifacts

For a new command `git <name>` (e.g., `git foo`, or for a multi-word command, `git push-all`):

1. **Script** — `bin/git-<name>`. Follow [`../shell-scripts/SKILL.md`](../shell-scripts/SKILL.md). Use [`bin/git-whoami`](../../bin/git-whoami) as the template for commands that take no options, or [`bin/gitex`](../../bin/gitex) for commands that parse flags. Make it executable: `chmod +x bin/git-<name>`.

2. **Test** — `test/test_git_<name>.py`. Follow [`../python-tests/SKILL.md`](../python-tests/SKILL.md). Use [`test/test_git_whoami.py`](../../test/test_git_whoami.py) as the canonical example. At minimum: cover the happy path, one error path, and argument validation.

   The filename mapping is load-bearing — `test_git_push_all.py` resolves to `bin/git-push-all` via the `bin` fixture (each `_` becomes `-`). A mismatched name silently fails to load the script.

3. **Usage doc** — `docs/usage/git-<name>.adoc`. Often already exists (stubbed upfront to drive the design). If so, verify the implementation matches; if not, create it. Follow [`../documentation/SKILL.md`](../documentation/SKILL.md).

4. **Validate** — run [`./check`](../../check) (see [`../testing/SKILL.md`](../testing/SKILL.md)). All three stages — ShellCheck, Ruff, pytest — must pass before commit.

## Indexes to sync

Three hand-maintained lists must stay aligned with the set of implemented commands:

- [`TODO.md`](../../TODO.md) — flip `[ ]` to `[x]` next to the command's entry.
- [`bin/gitex`](../../bin/gitex) — add a one-line entry under `_print_commands()`. Match the alphabetical ordering and two-space indent of existing entries.
- [`README.adoc`](../../README.adoc) and [`docs/usage/README.adoc`](../../docs/usage/README.adoc) — both list every command. Entries usually already exist because the usage doc was stubbed first; verify rather than blindly add.

## Commit

See [`../commits/SKILL.md`](../commits/SKILL.md). A new command is conventionally `feature: …`.
