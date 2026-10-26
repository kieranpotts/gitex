# `git cm`

Shortcut for `git add . && git commit` – stage and commit all changes in the working tree, including new (untracked) files. 

If a message is provided, it is used as the commit message; otherwise, the user will be prompted to input a message.

## Usage

```
$ git cm [<msg>] [--no-color]
```

Options:

- `--no-color`: Disable colored output. See [Colored output](../configuration.md#colored-output).
