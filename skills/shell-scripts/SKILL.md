# Shell scripts (`bin/` and `lib/`)

## Compliance

- POSIX-compliant. Scripts must work in Bash, Zsh, and Dash, and also WSL2 and Git-Bash-for-Windows. No Bashisms.
- Must pass `shellcheck --severity=style bin/* lib/*`.

## Script structure

Every script in `bin/` follows the structure of `bin/git-whoami`, used as the canonical reference:

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

`set -x` MAY be added temporarily for execution tracing during debugging, but MUST NOT be committed.

The **Dependencies** line in the header records external CLI tools the script invokes beyond Git itself and the standard POSIX utilities (e.g., `jq`, `curl`). Git, `lib/` files, and POSIX utilities (`grep`, `sed`, `awk`, `printf`, …) are assumed and not listed. If there are no such extras, write `None`.

## Shared libraries

- `lib/print.sh`: Helper functions for consistent messaging across commands. Sourced directly from `bin/` scripts.
- `lib/ansi-codes.sh`: Color variables (`$RED`, `$BOLD`, etc.). Used internally by `print.sh`; not sourced directly from `bin/` scripts.

## Output conventions

All user-facing output goes through `print_*` helpers from `lib/print.sh`. Do not call `echo` or `printf` directly for messages - raw output bypasses the project's color, stream, and prefix conventions.

| Helper | Stream | Use for |
| --- | --- | --- |
| `print_info` | stdout | Neutral informational output (e.g., "nothing to amend"). |
| `print_success` | stdout | Successful completion of an action. |
| `print_error` | stderr | Errors that caused the script to abort. |
| `print_warning` | stderr | Non-fatal warnings the user should see. |
| `print_hint` | stderr | A follow-up suggestion after an error (e.g., "Try 'gitex --help'"). |
| `print_prompt` | stdout + stderr | Interactive prompt before a `read`. |

Plain `echo` is acceptable only for the *data* a command produces (e.g., `git whoami` printing `name: …`). Anything that frames or annotates that data should use the helpers.

## Argument handling

Two patterns are used in `bin/`, both acceptable. Pick the one that matches the command's surface area:

**No-argument commands** ([`bin/git-whoami`](../../bin/git-whoami), [`bin/git-amend`](../../bin/git-amend)) reject all arguments up front:

```sh
main() {
  if [ $# -gt 0 ]; then
    print_error "git-<name> does not accept any options"
    return 1
  fi
  # ...
}
```

**Optioned commands** parse flags. For a fixed, small set of mutually exclusive flags, use a single `case` ([`bin/gitex`](../../bin/gitex)). For a richer surface with mixed positional and named arguments, use a `while/case` loop ([`bin/git-author`](../../bin/git-author)):

```sh
while [ $# -gt 0 ]; do
  case "$1" in
    --name)  author_name="$2"; shift 2 ;;
    --email) author_email="$2"; shift 2 ;;
    -*)      print_error "unknown option '$1'"; return 1 ;;
    *)       # positional handling
             shift ;;
  esac
done
```

Unknown options must produce `print_error "unknown option: …"` followed by `print_hint "Try '… --help' for more information."` where a `--help` is implemented.

## Defensive checks

Before performing a destructive operation (rewriting history, deleting refs, force-pushing), verify the precondition exists. Example from [`bin/git-amend`](../../bin/git-amend):

```sh
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
  print_error "no commits exist to amend"
  return 1
fi
```

Patterns to apply by default:

- Verify `HEAD` exists before any history-rewriting command.
- Use `git diff --cached --quiet` / `git diff --quiet` to distinguish staged vs. working changes.
- Use `git ls-files --others --exclude-standard` to detect untracked files.
- Redirect probing commands' stderr to `/dev/null` so the user only sees the script's own error messages.

## Cross-alias independence

Each script in `bin/` MAY depend on `lib/` files but MUST NOT depend on another `bin/` script. Users should be able to disable any subset of aliases (by deleting those `bin/` files) and have the remaining ones still work.
