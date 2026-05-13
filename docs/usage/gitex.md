# `gitex`

Get help with using GitEx.

This is the main help command for GitEx. It provides quick access to version information, lists currently implemented GitEx commands with descriptions, and shows usage instructions.

This command does not require a Git repository to run. You can use `gitex --version` or `gitex --commands` from any directory.

## Usage

```
$ gitex [--version|-v] [--commands|-c] [--help|-h]
```

### Options

`--version, -v`::
  Display the currently installed GitEx version number (read from `pyproject.toml`).

`--commands, -c`::
  List the implemented GitEx commands with brief descriptions.

`--help, -h`::
  Show usage instructions for the `gitex` command.

## Examples

Display version information:

```
$ gitex --version
GitEx version [major].[minor].[patch]
```

List currently implemented GitEx commands:

```
$ gitex --commands

GitEx commands:

  git amend
    Add all working changes to last commit, including new (untracked) files.

  git author [<ref>]
    Change the author of the last commit or an earlier specified commit.

  ...
```

Show help:

```
$ gitex --help
Usage: gitex [options]

Get help with GitEx.

Options:
  --version, -v   Show installed GitEx version number
  --commands, -c  List available GitEx aliases
  --help, -h      Show usage instructions

Examples:
  $ git gitex --version
  $ git gitex --commands
  $ git -h
```

Help information is also returned when the `gitex` command is run without any arguments.
