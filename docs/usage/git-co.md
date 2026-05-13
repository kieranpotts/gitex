# `git co`

Shortcut for `git checkout`. All parameters are forwarded to the underlying `git checkout` command.

This is a convenience alias for one of Git's most frequently used commands. It saves typing while providing full access to all `git checkout` functionality.

## Usage

```
$ git co [...]
```

## Examples

Switch to an existing branch:

```
$ git co feature-branch
```

Create a new branch and switch to it:

```
$ git co -b new-feature
```

Force-create a branch (overwrites if it exists):

```
$ git co -B hotfix
```

Switch to the previous branch:

```
$ git co -
```

Checkout a specific commit (detached HEAD):

```
$ git co a1b2c3d
```

Create a branch from a specific commit:

```
$ git co -b feature-x a1b2c3d
```

See [git-checkout](https://git-scm.com/docs/git-checkout) for further documentation.

## See also

- [git-switch](https://git-scm.com/docs/git-switch): Modern alternative for switching branches.
- [git-restore](https://git-scm.com/docs/git-restore): Modern alternative for restoring files.
