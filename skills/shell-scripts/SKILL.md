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

## Shared libraries

- `lib/print.sh` — Helper functions for consistent messaging across commands. Sourced directly from `bin/` scripts.
- `lib/ansi-codes.sh` — Color variables (`$RED`, `$BOLD`, etc.). Used internally by `print.sh`; not sourced directly from `bin/` scripts.

## Cross-alias independence

Each script in `bin/` MAY depend on `lib/` files but MUST NOT depend on another `bin/` script. Users should be able to disable any subset of aliases (by deleting those `bin` files) and have the remaining ones still work.
