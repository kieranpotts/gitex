# Configuration

GitEx commands can be configured using environment variables.

## Colored output

GitEx uses color to highlight errors, warnings, hints, and success messages. Color is decided separately for stdout and stderr, using these rules in order of precedence:

1. Color is disabled if the `--no-color` option is passed to the command, or if the `GITEX_NO_COLOR` or `NO_COLOR` environment variable exists.
2. Otherwise, color is enabled if the `FORCE_COLOR` environment variable exists.
3. Otherwise, color is enabled only if the stream is an interactive terminal (a TTY). Output that is piped to another program or redirected to a file is not colored.

Anything that disables color always wins, so `--no-color` turns color off even if `FORCE_COLOR` is set in your shell. For all three environment variables, only the variable's existence matters, not its value. Setting `NO_COLOR=0` or `NO_COLOR=` still disables color.

Every GitEx command accepts the `--no-color` option, except the shortcuts that forward their parameters to Git ([`git cl`](./usage/git-cl.md), [`git co`](./usage/git-co.md), and [`git sw`](./usage/git-sw.md)).

These settings control the messages that GitEx prints itself. Output from the Git commands that GitEx runs is colored according to your Git configuration (see [`color.ui`](https://git-scm.com/docs/git-config#Documentation/git-config.txt-colorui)).

## Environment variables

### `GITEX_DEFAULT_REMOTE_NAME`

Specifies the name of the default remote repository for operations that push to or fetch from a remote.

**Default value:** `origin`

**Used by:** `git-br`

**Example:**

```
# Set in your shell configuration file (~/.bashrc, ~/.zshrc, etc.).
export GITEX_DEFAULT_REMOTE_NAME=upstream

# Or set for a single command.
GITEX_DEFAULT_REMOTE_NAME=upstream git br my-feature
```

This is useful when working with repositories that use a different remote naming convention, such as "upstream" instead of "origin", for the default remote repository.

### `GITEX_NO_COLOR`

Disables colored output from GitEx commands only, if the variable exists. It has the same effect as passing `--no-color` to every command. See [Colored output](#colored-output).

**Default value:** Not set.

**Used by:** All commands that accept `--no-color`.

**Example:**

```
# Disable color for GitEx, but not for other programs.
export GITEX_NO_COLOR=1
```

### `NO_COLOR`

Disables colored output, if the variable exists. This is a [cross-program convention](https://no-color.org/), so setting it typically disables color in other command-line programs as well as GitEx. See [Colored output](#colored-output).

**Default value:** Not set.

**Used by:** All commands that accept `--no-color`.

**Example:**

```
export NO_COLOR=1
```

### `FORCE_COLOR`

Enables colored output, if the variable exists, even when output is not going to a terminal. This is useful when piping into a program that renders color itself, such as a pager. `FORCE_COLOR` is overridden by `--no-color`, `GITEX_NO_COLOR`, and `NO_COLOR`. See [Colored output](#colored-output).

**Default value:** Not set.

**Used by:** All commands that accept `--no-color`.

**Example:**

```
FORCE_COLOR=1 git orphan gh-pages 2>&1 | less -R
```
