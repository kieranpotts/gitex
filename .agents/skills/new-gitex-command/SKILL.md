---
name: new-gitex-command
description: >-
  Create a new GitEx command from scratch. Scaffolding may or may not already
  exist. Write new tests and usage docs.
compatibility: >-
  requires Read, Write, Edit, Glob, Grep, Bash (./run/check, chmod, dash)
license: MIT
---

# New GitEx command

Create a new GitEx command from scratch, including its tests and usage docs.
Extend existing scaffolding artifacts, if they already exist, otherwise
create new artifacts by following existing conventions and documented
standards.

## Parameters

Determine the following information from the session context and local
environment, if possible. If you're uncertain about the required parameters,
prompt the user for clarification.

- **Command name — REQUIRED.** The `<name>` in `git <name>`, eg. `sync` or
  `push-all`.

- **Command parameters — OPTIONAL.** Options and flags that may be passed to the
  new command. The parameters may be unique to the custom command, and/or they
  may be forwarded to the underlying Git-native commands used in the Git alias
  script. If not specified, assume the GitEx command takes no parameters.

## Success criteria

- An executable `bin/git-<name>` MUST exist.

- `test/test_git_<name>.py` MUST hold passing tests, covering full argument
  validation (including `--no-color`), all of the happy paths, and at least
  one error path.

- `docs/usage/git-<name>.md` MUST exist and describe the implemented behavior
  from the perspective of an end user of the new Git command.

- `./run/check` MUST exit 0.

- `dash bin/git-<name>` MUST behave as the tests expect, and produce the same
  exit status and output as `bash bin/git-<name>`.

- The new command MUST appear in the output from `_print_commands()` in
  `bin/gitex`.

- The new command MUST be listed in this repository's top-level `README.md`.

- The new command MUST be listed in `docs/usage/README.md`, with a ✅ beside it.

- There MUST NOT be any `TODO` command markers left in any of the new artifacts.

- There MUST NOT be any commented-out code in any of the new artifacts.

## Step-by-step instructions

1.  Find out what already exists for the command. The following scaffolding may
    or may not already exist.

    - A draft `bin/git-<name>` file, marked `# TODO: DRAFT IMPLEMENTATION`.

    - A placeholder `test/test_git_<name>.py`, with its test body commented out.

    - A usage doc, `docs/usage/git-<name>.md`, recording the intended interface.

2.  Write or finish `bin/git-<name>`. Make it executable with `chmod +x`.
    Implement the interface described in the prompt or in the existing usage
    doc. Copy the structure of the existing script whose interface is closest
    to the one you need. Examples:

    - `bin/git-whoami`, for a command that takes no arguments except `--no-color`.
    - `bin/git-amend`, for the simplest form of the parse-then-act pattern.
    - `bin/gitex`, for a small fixed set of flags with `--help` and `--version`.
    - `bin/git-orphan`, for an optional positional argument plus flags and `--help`.
    - `bin/git-author`, for options that take values, and repeated options.

3.  Write `test/test_git_<name>.py`. Use `test/test_git_whoami.py` as the model
    implementation.

4.  Write or update `docs/usage/git-<name>.md`, bringing it into line with the
    actual implementation.

5.  Add the command to the following indexes.

    - In `bin/gitex` add an entry to `_print_commands()`, in alphabetical order,
      matching the existing entries' synopsis line and indented one-line
      summary.

    - `docs/usage/README.md`. Add a ✅ after the command's link.

    - `README.md`. Check the command is listed, and is placed in alphabetical
      order.

6.  Run `./run/fix`, then `./run/check`. Fix any failure and run them again,
    until `./run/check` passes.

7.  Run the new GitEx command under Dash, in a throwaway repository, for the
    main happy paths and one error path. For each run, compare the exit status
    and output with an equivalent run under Bash. Remember to pass the script's
    absolute path, so that it can find `lib/print.sh` relative to itself.

    ```sh
    gitex_dir="$(pwd)"
    cd "$(mktemp -d)" && git init --quiet
    dash "${gitex_dir}/bin/git-<name>" [args]
    bash "${gitex_dir}/bin/git-<name>" [args]
    ```

> [!NOTE]
> The purpose of running the command under Dash is to catch any bashisms that
> ShellCheck may have missed. The test suite runs the scripts under Bash, so
> it will not catch bashisms. Dash adds few POSIX extensions, so running the
> GitEx scripts under this shell is close to a compliance test.

## Rules

- You MUST NOT commit, stage, or push your changes. Leave them dirty in the
  working tree for the user to review before committing.

- The test file name MUST map exactly to the script name. A mismatched test
  file name fails all its tests.

- A multi-word command MUST be kebab-case in its script name, eg.
  `bin/git-push-all`, and snake_case in its test file name, eg.
  `test/test_git_push_all.py`.

## Edge cases

- If there are inconsistencies between how the new command's interface is
  described by the user (in their prompt) and how it is defined in the draft
  usage doc or in the placeholder implementation, stop and prompt the user
  to clarify the intended behavior.

## Examples

- A complete change set for the GitEx command `git foo`:

  ```text
  bin/git-foo              The Git alias itself.
  bin/gitex                One entry added to _print_commands().
  docs/usage/README.md     ✅ added alongside the `git foo` entry.
  docs/usage/git-foo.md    Brought in line with the implementation.
  test/test_git_foo.py     Placeholder replaced with live tests.
  ```

## Assets

- [Usage doc template](./assets/documentation/usage-doc-template.md) \
  The skeleton for a new `docs/usage/git-<name>.md` file.

## References

- [Shell scripts](./references/shell-scripts.md) \
  Template, messaging, option-parsing, and safety conventions for the scripts
  in `bin/` and `lib/`.

- [POSIX portability](./references/posix-portability.md) \
  Shell language and utility rules that keep the GitEx scripts portable between
  different Unix shells.

- [Python tests](./references/python-tests.md) \
  Naming, fixtures, test shape, coverage rules, and gotchas for the pytest
  suite in `test/`.

- [Running checks](./references/running-checks.md) \
  How to run `./run/fix` and `./run/check`, and diagnose their failures.

- [User documentation](./references/user-documentation.md) \
  Style guide for all user-facing Markdown documentation.
