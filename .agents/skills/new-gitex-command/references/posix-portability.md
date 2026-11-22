# POSIX shell portability

Read this before writing or reviewing any shell code in `bin/` or `lib/`. This
extends the [shell scripts](./references/shell-scripts.md) reference guide.

GitEx scripts MUST run and function consistently under Bash, Zsh, and Dash, and
also under Git Bash for Windows and WSL2. This means the GitEx scripts are
limited to the POSIX shell language and POSIX-compatible utilities.

Unfortunately, we cannot rely only on the linter and tests to validate the
GitEx scripts for POSIX compliance — for the following reasons.

* Bash invoked as `sh` runs in POSIX mode, but POSIX mode does not disable
  Bash's extensions. `local`, `[[ ]]`, and arrays all still work!

* The pytest suite runs every script with `bash <script>`, so it does not catch
  bashisms.

* ShellCheck catches most bashisms, but not all.

* Dash implements very few shell extensions, which makes a run under Dash the
  closest thing to a POSIX compliance test. But even Dash accepts `local`.

So, you MUST NOT rely on the linter and tests to validate POSIX compliance. You
need to use your judgment, too. Follow all the rules for POSIX compliance
described below.

## Shebang and shell options

- GitEx scripts MUST use `#!/bin/sh`, never `#!/bin/bash`, and never
  `#!/bin/env sh`. `/bin/env` exists only on Linux distributions that merge
  `/bin` into `/usr/bin`. It is absent on macOS, the BSDs, and Alpine.

- GitEx scripts MUST have `set -eu` on the line after the shebang, before any
  other logic. `-e` exits on any unhandled non-zero status. `-u` makes a
  reference to an unset variable an error.

- GitEx scripts MUST NOT use `set -o pipefail`. It is not POSIX. Where a
  pipeline's earlier stages can fail, run them separately and check each one.

## Bashisms and their POSIX replacements

GitEx scripts MUST have the following bashisms replaced my the mapped POSIX
replacements.

| Bashism                                                    | POSIX replacement                                                     |
| ---------------------------------------------------------- | --------------------------------------------------------------------- |
| `[[ … ]]`                                                  | `[ … ]`, quoting every operand                                        |
| `==` in a test                                             | `=`                                                                   |
| `[[ $x =~ re ]]`                                           | `case` with a glob pattern, or `grep -E`                              |
| `local name`                                               | A name unique to the function, eg. prefixed with its purpose          |
| `function name { … }`                                      | `name() { … }`                                                        |
| Arrays                                                     | The positional parameters (`set -- …`), or a newline-separated string |
| `source file`                                              | `. file`                                                              |
| `echo -e`, `echo -n`                                       | `printf`                                                              |
| `$'…'` strings                                             | `printf` with escape sequences                                        |
| `<<< "$var"`                                               | `printf '%s\n' "${var}" \|`                                           |
| `<( … )`                                                   | A pipe, or a temporary file from `mktemp`                             |
| `&> file`                                                  | `> file 2>&1`                                                         |
| `read -p "Prompt"`                                         | `printf` the prompt, then `read -r`                                   |
| `(( … ))`, `let`                                           | `$(( … ))` arithmetic expansion inside a `[ ]` test or assignment     |
| `${var^^}`, `${var,,}`                                     | `printf '%s' "${var}" \| tr '[:lower:]' '[:upper:]'`                  |
| `${var:offset:length}`                                     | `${var#…}` and `${var%…}`, or `cut`                                   |
| `${!name}`                                                 | Restructure the code. Indirection needs `eval`, which is banned       |
| `{1..5}`                                                   | A `while` loop with a counter                                         |
| `$RANDOM`, `declare`, `typeset`, `pushd`, `popd`, `select` | No equivalent. Restructure the code                                   |

## Variables

- Under `set -u`, a parameter that may be absent MUST be read with a default,
  eg. `"${2:-}"`. To test whether a variable is set, even to the empty string,
  use `[ -n "${NAME+x}" ]`.

- Without `local`, every variable is global. Therefore, each GitEx function's
  working variables MUST have names that cannot clash with those of any another
  function.

## Functions and exit status

- GitEx scripts MUST use `return <n>` inside functions and `exit <n>` at the top
  level. `return` outside a function is undefined in POSIX, and Dash rejects
  it.

## Commands and output

- GitEx scripts MUST NOT use GNU-only flags, which fail on macOS and the BSDs,
  eg. `sed -i`, `grep -P`, `readlink -f`, `date -d`, `xargs -r`

- For the same reason, GitEx scripts MUST NOT use long options such as `--color` on
  non-Git utilities.

- GitEx scripts MUST use `printf` for any output containing escapes, or a variable
  that might begin with `-`. Plain `echo` with a fixed string MAY be used.
