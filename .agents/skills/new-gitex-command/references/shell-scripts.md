# Shell scripts

You MUST read this before writing or reviewing any script in `bin/` or `lib/`,
together with the [POSIX portability](./posix-portability.md) reference.

These rules do not apply to the devtool scripts in `run/`, which ShellCheck
also does not scan.

## Template

A new `bin/` script MUST be executable, and MUST start from the following
template.

```sh
#!/bin/sh
set -eu

#
# git-<name> - One-line description.
#
# Extended description, in prose. Multiple paragraphs are allowed. Hard-wrap
# at 80 characters.
#
# Usage:
#   $ git <name> [<arg>] [--no-color]
#
# Dependencies: (none)
#

# shellcheck source=../lib/print.sh
. "$(dirname "$0")/../lib/print.sh"

main() {
  # Parse the command line, then act on it.
  :
}

main "$@"
```

The `Dependencies` line MUST list every external program the script invokes,
eg. `jq, curl`, or `(none)`. Git, files in `lib/`, and POSIX utilities are
assumed and SHOULD NOT be explicitly listed as dependencies.

## Self-containment

A `bin/` script MUST NOT source or call another `bin/` script. It MUST source
nothing but files in `lib/`.

Users can disable a GitEx command simply by deleting its file from `bin/`.
So each script MUST work on its own. All shared code MUST go in `lib/`.

## Messages

- User-facing messages MUST go through the helpers in `lib/print.sh`, which
  handle color and choose the stream.

  - `print_info`. Neutral information, to stdout.
  - `print_success`. A completed action, to stdout, prefixed `success:`.
  - `print_error`. The error that stopped the command, to stderr, prefixed `error:`.
  - `print_warning`. A non-fatal side effect, to stderr, prefixed `warning:`.
  - `print_hint`. Advice on what to do next, to stderr, in cyan.
  - `print_prompt`. The prompt before a `read`.

  A `print_hint` SHOULD follow every `print_error` and `print_warning`.

  Plain `echo` or `printf` MUST be kept for the command's data output, eg. the
  `name: …` lines of `git whoami`, so that the data stays clean when piped.

- Every message MUST be written as one or more full sentences. Each sentence
  starts with a capital letter (unless it starts with a literal identifier such
  as `--name` or `git-amend`) and ends with a period.

  An error SHOULD be one short sentence, with advice moved to a following
  `print_hint`.

  Prompts MUST end with a colon instead, eg. `Author's name:`.

  ```text
  error: --name requires a value.
  Try 'git author --help' for more information.
  ```

- A `bin/` script MUST NOT source `lib/ansi-codes.sh` or emit raw color codes.
  Where a new kind of colored output is needed, add a `print_*` helper to
  `lib/print.sh`, which owns the rules for when color is enabled.

## Option parsing

- A script MUST parse its whole command line before acting on any of it, so
  that the order of arguments never changes what the command does. Inside the
  parse loop, the script MUST only set variables and record the first usage
  error. It MUST NOT print, `return`, or `exit` until the loop ends. It MUST
  then act in the following order.

  1. Presentation flags such as `--no-color`. `disable_color` only sets a
     variable, so it is safe to call inside the loop.

  2. `--help`, which MUST take precedence over every other option and every
     usage error.

  3. `--version`, where implemented.

  4. Usage errors.

  5. The command itself.

- Contradictory options, including a value-taking option given twice, eg.
  `--name a --name b`, MUST be a usage error rather than "last one wins".

- A script that implements `--help` MUST follow an unknown-option error with
  `print_hint "Try 'git <name> --help' for more information."`.

## Destructive operations

A script MUST check its preconditions before any destructive Git operation —
rewriting history, deleting refs, force-pushing, or discarding work — and stop
with an error if they do not hold.

- The script MUST verify that `HEAD` exists with
  `git rev-parse --verify HEAD` before rewriting history.

- The script SHOULD tell staged changes from working changes with
  `git diff --cached --quiet` and `git diff --quiet`.

- The script SHOULD detect untracked files with
  `git ls-files --others --exclude-standard`.

- The script MUST find the repository with `git rev-parse --git-dir`, and MUST
  NOT test for a `.git` directory, which is a file in a worktree or submodule.

## Variables and naming

- Variables and functions MUST be named in `lower_snake_case`. `UPPER_CASE`
  MUST be reserved for variables exported to the environment, such as
  `GITEX_NO_COLOR`, so that script variables cannot collide with environment
  variables.

- Names SHOULD be descriptive, eg. `branch_name` over `b`.

- Every expansion MUST be quoted, eg. `"${name}"`, `"$1"`, `"$(command)"`.
  Quoting prevents word splitting and glob expansion. Where splitting is
  intended, the expansion MAY be left unquoted, but a comment MUST say why.

- Named variables SHOULD use braces, `"${name}"` rather than `"$name"`, as the
  GitEx scripts do. Positional parameters SHOULD be written bare, `"$1"`.

## Functions and exit status

- The logic of every script MUST be wrapped in `main()`, called at the end of
  the file as `main "$@"`.

- Functions MUST return an explicit status, 0 for success and non-zero for
  failure, rather than relying on whatever the last command returned. `return`
  takes only an integer from 0 to 255. Data MUST be returned by writing it to
  stdout, and captured with `$( … )`.

- Under `set -e`, a failing command inside an `if` condition, or on the left of
  `&&` or `||`, does not exit the script. A script SHOULD use that to handle an
  expected failure explicitly:

  ```sh
  if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
    print_error "No commits exist to amend."
    return 1
  fi
  ```

## Commands

- Command substitution MUST use `$( … )` and MUST NOT use backticks. It nests
  without escaping.

- Scripts SHOULD prefer shell built-ins, such as parameter expansion, over
  external commands for simple string work.

- Scripts MUST NOT use `eval`. It makes it impossible to reason about what the
  script runs. Scripts MUST NOT use aliases. They are not reliably expanded in
  non-interactive shells. Define a function instead.

- Changes MUST NOT be committed with `set -x`. It MAY be used temporarily for
  debugging.

## ShellCheck

- You MUST run ShellCheck at "style" severity. Run
  `mise exec -- shellcheck --severity=style bin/* lib/*`.

- A sourced file MUST be pointed to with a `source` directive, relative to the
  current file.

  ```sh
  # shellcheck source=../lib/print.sh
  . "$(dirname "$0")/../lib/print.sh"
  ```

- A check MUST be disabled only on the line that needs it, and a comment beside
  it MUST explain why.

  ```sh
  # Word splitting is intended here. $flags holds multiple separate options.
  # shellcheck disable=SC2086
  git log $flags
  ```

## Other conventions

- Probing commands SHOULD redirect their stderr to `/dev/null`, so that the
  user sees only the script's own messages.

- Helper functions private to a script SHOULD be named with a leading
  underscore, eg. `_print_help` or `_usage_error`.

## Edge cases

- If the script is an un-reviewed draft, marked
  `# TODO: DRAFT IMPLEMENTATION`, then you MUST treat its code as a rought
  sketch. Drafts often contain bashisms and some do not even run. You MUST check
  every line against the POSIX reference rather than assuming it is sound.

- If a test passes but the script fails when run as `git <name>`, then you
  SHOULD suspect the shebang or a bashism. The test suite runs every script with
  `bash <script>`, ignoring its shebang, so neither can fail there.
