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

    - `print_info`: Streams to stdout neutral informational output in prose. Example: "There's nothing to amend. The working tree is clean."

    - `print_success`: Streams to stdout notifications of successful completion of an action. Example: "success: Switched to new orphan branch 'gh-pages'.".

    - `print_error`: Streams to stderr errors that caused the script to abort. Example: "error: --name requires a value.". RECOMMENDED to be followed by `print_hint`.

    - `print_warning`: Streams to stderr non-fatal, non-blocking side-effects that the user should be notified of. Example: "warning: Your working changes were staged.". RECOMMENDED to be followed by `print_hint`.

    - `print_hint`: Streams to stderr a follow-up suggestion in prose. Example: "Try 'gitex --help' for more information.". Text color is cyan. RECOMMENDED for use after `print_error` and `print_warning`.

    - `print_prompt`: Interactive prompt before a `read`. Example: "Your email address:".

    Plain `echo` / `printf` is reserved for the command's *data* output (eg. `git whoami` printing `name: …`). Anything that frames or annotates that data uses the helpers.

-   **Write messages as proper sentences.**

    Every message — error, warning, success, info, and hint — is written as one or more proper English sentences, per TS-16 (Command Line Interfaces), section "Error message content". Start each sentence with a capital letter, unless it starts with a literal identifier such as `--name` or `git-amend`, which keeps its own case. End each sentence with a period. Keep the error itself to one short sentence, and put advice on what to do next in a following `print_hint`. The helpers prefix errors, warnings, and success messages with the message type (`error: `, `warning: `, or `success: `). Examples:

    ```
    error: Failed to read config.
    ```

    ```
    There's nothing to amend. The working tree is clean.
    ```

    Write prompts like this:

    ```
    Author's name:
    ```

    Use the `print_error`, `print_warning`, `print_success`, `print_info`, `print_hint`, and `print_prompt` utilities consistently.

-   **Do not source `lib/ansi-codes.sh` directly from `bin/` scripts.**

    `lib/ansi-codes.sh` is an internal dependency of `print.sh`. If you find yourself wanting raw color codes, the right answer is usually a new `print_*` helper.

-   **Pick an argument-handling pattern matching the command's API.**

    Follow the patterns in the [POSIX skill](https://raw.githubusercontent.com/kieranpotts/skills/refs/heads/dev/skills/code/posix/SKILL.md), but replace `printf … >&2` with `print_error`.

    Where `--help` is implemented, output unknown-option errors with `print_hint "Try 'git <command> --help' for more information."`.

-   **Parse the whole command line before acting on any of it.**

    Per TS-16 (Command Line Interfaces), the order of flags MUST NOT change what a command does, including which messages it prints and whether they are colored. So `git amend bogus --no-color` and `git amend --no-color bogus` print the same uncolored error.

    Inside the parse loop, only record what was given: set variables, and record the first usage error rather than printing it. Do not print, `return`, or `exit` until the loop has finished. Then act in this order:

    1. Presentation flags such as `--no-color`. (`disable_color` only sets a variable, so it is safe to call inside the loop.)
    2. `--help`, which beats every other option and every usage error.
    3. `--version`, where implemented.
    4. Usage errors.
    5. The command itself.

    Flags that contradict each other, including the same value-taking flag given twice (eg. `--name a --name b`), are a usage error, not "last one wins". See `bin/git-amend` for the simplest form of the pattern, and `bin/git-orphan` and `bin/gitex` for `--help` and `--version` precedence.

-   **Add defensive checks before destructive Git operations.**

    Verify preconditions before rewriting history, deleting refs, or force-pushing, eg.:

    ```sh
    if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
      print_error "No commits exist to amend."
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
  print_error "Not inside a Git repository."
  return 1
fi
```

## References

- [POSIX shell scripting skill](https://raw.githubusercontent.com/kieranpotts/skills/refs/heads/dev/skills/code/posix/SKILL.md)
