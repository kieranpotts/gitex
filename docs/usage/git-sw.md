# `git sw`

Shortcut for `git switch`. All parameters are forwarded to the underlying `git switch` command.

`git switch` is the modern, focused alternative to `git checkout` for switching branches. It was introduced in Git 2.23 to provide a clearer, safer interface for branch operations without the complexity of `git checkout`.

## Usage

```
$ git sw [...]
```

## Examples

Switch to an existing branch:

```
$ git sw feature-branch
```

Create a new branch and switch to it:

```
$ git sw -c new-feature
```

Force-create a branch (overwrites if it exists):

```
$ git sw -C hotfix
```

Switch to the previous branch:

```
$ git sw -
```

See [git-switch](https://git-scm.com/docs/git-switch) for further documentation.

## See also

- [git-checkout](https://git-scm.com/docs/git-checkout): Legacy command with broader functionality.
- [git-restore](https://git-scm.com/docs/git-restore): Modern alternative for restoring files.
- [`git co`](./git-co.md): GitEx shortcut for `git checkout`.
