---
name: shell-scripts
description: Coding conventions and design patterns for the POSIX shell scripts in bin/ and lib/.
compatibility: requires sh, shellcheck
license: MIT
---

# Shell scripts

Use this skill when authoring or modifying a script in `bin/` or `lib/`.

This skill extends the [POSIX shell scripting skill](https://raw.githubusercontent.com/kieranpotts/skills/refs/heads/dev/skills/code/posix/SKILL.md) – all rules there apply here. This skill covers GitEx-specific conventions.

Do NOT use this skill for the root-level `./check` and `./fix` scripts, which have looser conventions and are not scanned by ShellCheck.

Do NOT use this skill for Python tests.

## Rules

-   **Base new scripts on this template:**

    ```sh
    #!/bin/env sh
    set -eu

    #
    # <command-name> - One-line description.
    #
    # Extended usage docs. Multiple paragraphs supported.
    # Markdown syntax. Hard-wrap lines.
    #
    # Usage:
    #   $ git <command> [args]
    #
    # Dependencies: <list, or "(none)">
    #

    # shellcheck source=../lib/print.sh
    . "$(dirname "$0")/../lib/print.sh"

    main() {
      # ...
    }

    main "$@"
    ```

    The "Dependencies" line records external CLI tools the script invokes (eg. `jq, curl`). `git`, `lib/*` files, and POSIX built-ins like `grep`, `sed`, `awk`, and `printf` are assumed and NOT listed as dependencies. Write `(none)` if the script uses nothing except `git`, `lib/*` files, and POSIX built-ins.

-   **Each `bin` script MUST be self-contained.**

    Each `bin/` script MAY depend on `lib/` files but MUST NOT depend on another `bin/` script.

    Users can disable any subset of aliases by deleting `bin/` files. This means that each `bin` script MUST be treated as a self-contained binary. Only `lib/*` files MAY be sourced from `bin` scripts.

-   **Use `print_*` helpers for all user-facing output.**

    Sourcing `lib/print.sh` exposes:

    - `print_info`: Streams to stdout neutral informational output in prose. Example: "Nothing to amend. The working tree is clean."

    - `print_success`: Streams to stdout notifications of successful completion of an action. Example: "success: new branch: <branch-name>".

    - `print_error`: Streams to stderr errors that caused the script to abort. Example: "--name is invalid". RECOMMENDED to be followed by `print_hint`.

    - `print_warning`: Streams to stderr non-fatal, non-blocking side-effects that the user should be notified of. Example: "warning: your working changes were staged". RECOMMENDED to be followed by `print_hint`.

    - `print_hint`: Streams to stdout a follow-up suggestion in prose. Example: "Try 'gitex --help'". Same as `print_info` except text color is cyan. RECOMMENDED for use after `print_error` and `print_warning`.

    - `print_prompt`: Interactive prompt before a `read`. Example: "Your email address:".

    Plain `echo` / `printf` is reserved for the command's *data* output (eg. `git whoami` printing `name: …`). Anything that frames or annotates that data uses the helpers.

-   **Write Go-style messages.**

    For errors and warnings, and success messages, write one sentence per error, start lowercase, and do not terminate with a period or other punctuation mark. Prefix with the message type: `error: `, `warning: `, or `success: `. Example:

    ```
    error: failed to read config
    ```

    But for more general output with extended information, instructions, or hints, write proper English sentences. Example:

    ```
    There's nothing to amend. The working tree is clean.
    ```

    Write prompts like this:

    ```
    Author's name:
    ```

    Use the `print_error`, `print_warning`, `print_success`, `print_info`, `print_help`, and `print_prompt` utilities consistently.

-   **Do not source `lib/ansi-codes.sh` directly from `bin/` scripts.**

    `lib/ansi-codes.sh` is an internal dependency of `print.sh`. If you find yourself wanting raw color codes, the right answer is usually a new `print_*` helper.

-   **Pick an argument-handling pattern matching the command's API.**

    Follow the patterns in the [POSIX skill](https://raw.githubusercontent.com/kieranpotts/skills/refs/heads/dev/skills/code/posix/SKILL.md), but replace `printf … >&2` with `print_error`.

    Where `--help` is implemented, output unknown-option errors with `print_hint "Try 'git <command> --help' for more information."`.

-   **Add defensive checks before destructive Git operations.**

    Verify preconditions before rewriting history, deleting refs, or force-pushing, eg.:

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

-   **Validate.**

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

- [POSIX shell scripting skill](https://raw.githubusercontent.com/kieranpotts/skills/refs/heads/dev/skills/code/posix/SKILL.md)
