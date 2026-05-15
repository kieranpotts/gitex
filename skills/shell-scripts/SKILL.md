---
name: shell-scripts
description: Coding conventions and design patterns for the POSIX shell scripts in bin/ and lib/.
compatibility: requires sh, shellcheck
license: MIT
---

# Shell scripts

Use this skill when authoring or modifying a script in `bin/` or `lib/`. This skill extends the [POSIX shell scripting skill](https://github.com/kieranpotts/skills/blob/dev/skills/code/posix/SKILL.md) — all rules there apply here. This document covers GitEx-specific conventions.

Do NOT use this skill for the root-level `check` / `fix` scripts, which have looser conventions and are not scanned by ShellCheck, or for Python tests.

## Rules

- **Base new scripts on this template:**

  ```sh
  #!/bin/env sh
  set -eu

  #
  # <command-name> - <one-line description>.
  #
  # <Longer description if needed.>
  #
  # Usage:
  #   $ git <command> [args]
  #
  # Dependencies: <list, or "None">
  #

  # shellcheck source=../lib/print.sh
  . "$(dirname "$0")/../lib/print.sh"

  main() {
    # ...
  }

  main "$@"
  ```

  The **Dependencies** line records external CLI tools the script invokes beyond Git and the standard POSIX utilities (eg. `jq`, `curl`). Git, `lib/` files, and POSIX utilities (`grep`, `sed`, `awk`, `printf`, …) are assumed and not listed. Write `None` if the script uses nothing beyond built-ins.

- **Each `bin` script MUST be self-contained.**

  Each `bin/` script MAY depend on `lib/` files but MUST NOT depend on another `bin/` script.

  Users can disable any subset of aliases by deleting those `bin/` files. This means that each `bin` script MUST be treated as a self-contained binary (with the exception of dependencies on `lib/*` files).

- **Use `print_*` helpers for all user-facing output.**

  Sourcing `lib/print.sh` exposes:

  - `print_info`: Streams to stdout neutral informational output (eg. "nothing to amend").

  - `print_success`: Streams to stdout notifications of successful completion of an action.

  - `print_error`: Streams to stderr errors that caused the script to abort.

  - `print_warning`: Streams to stderr non-fatal warnings the user should see.

  - `print_hint`: Streams to stderr a follow-up suggestion after an error (eg. "Try 'gitex --help'").

  - `print_prompt`: Interactive prompt before a `read`.

  Plain `echo` / `printf` is reserved for the command's *data* output (eg. `git whoami` printing `name: …`). Anything that frames or annotates that data uses the helpers.

- **Do not source `lib/ansi-codes.sh` directly from `bin/` scripts.**

  `lib/ansi-codes.sh` is an internal dependency of `print.sh`. If you find yourself wanting raw color codes, the right answer is usually a new `print_*` helper.

- **Pick an argument-handling pattern matching the command's surface.**

  Follow the patterns in the [POSIX skill](https://github.com/kieranpotts/skills/blob/dev/skills/code/posix/SKILL.md), but replace `printf … >&2` with `print_error`.

  Where `--help` is implemented, follow unknown-option errors with `print_hint "Try 'git <command> --help' for more information."`.

- **Add defensive checks before destructive Git operations.**

  Verify preconditions before rewriting history, deleting refs, or force-pushing. Pattern from `bin/git-amend`:

  ```sh
  if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
    print_error "no commits exist to amend"
    return 1
  fi
  ```

  Common Git preconditions:

  - Verify `HEAD` exists before any history-rewriting command.

  - Use `git diff --cached --quiet` / `git diff --quiet` to distinguish staged vs. working changes.

  - Use `git ls-files --others --exclude-standard` to detect untracked files.

  - Redirect probing commands' stderr to `/dev/null` so the user only sees the script's own error messages.

- **Validate.**

  Every script must pass `shellcheck --severity=style bin/* lib/*`.

  Use the `./check` and `./fix` helpers.

  While ShellCheck observes a script's shebang line (`#!`), `pytest` invokes `bash <script>` and does not scope the shell to the constraints of the shebang. Therefore, a broken shebang will pass tests and fail in real-world `PATH` invocations. Manual verification of the `bin` scripts is therefore REQUIRED.

## Examples

Sourcing helpers and emitting an error:

```sh
# shellcheck source=../lib/print.sh
. "$(dirname "$0")/../lib/print.sh"

if [ ! -d ".git" ]; then
  print_error "not inside a Git repository"
  return 1
fi
```

## References

- [POSIX shell scripting skill](https://github.com/kieranpotts/skills/blob/dev/skills/code/posix/SKILL.md): the upstream generic skill this one extends.
