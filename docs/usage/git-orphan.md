# `git orphan`

Create an orphaned branch, with no parent commits, and switch to it.

This is useful to start a fresh trunk that is not based on any previous work. You might use this, for example, to create a `gh-pages` branch as a build target, but which is otherwise unconnected to the history of the source branches.

By default, the files of the previously checked-out branch, plus any working changes, including untracked files, are carried over to the new branch and staged, ready for its first commit. Nothing is lost.

If the `--fresh` option is provided, the index and working tree are cleared instead, so the new branch starts empty. Tracked files, staged changes, unstaged changes, and untracked files are all deleted. Ignored files are kept. If there are any uncommitted changes or untracked files, they are listed and you are asked to confirm before anything is deleted. Answering anything other than `y` aborts the operation without making any changes.

Unlike [`git br`](./git-br.md), the new branch is not pushed upstream. Until there is at least one commit in the orphaned branch's history, there is nothing to push.

> [!CAUTION]
> Be careful about using the `--fresh` option. If you confirm the prompt, uncommitted work-in-progress is deleted and cannot be recovered with Git. Be sure you have committed everything you want to keep before running this command.

## Usage

```
$ git orphan [<branch>] [--fresh]
```

If no branch name is provided, you will be prompted to enter one interactively.

The operation will fail if the branch name is invalid or already exists.

Options:

- `--fresh`: Clear the index and working tree, except ignored files.
- `--help`, `-h`: Show usage instructions.

## Examples

Start a new orphan branch, keeping the current files staged for its first commit:

```
$ git orphan gh-pages
success: Switched to new orphan branch 'gh-pages'.
All files in the working tree are staged, ready for the first commit.
```

Start a new orphan branch with an empty working tree:

```
$ git orphan gh-pages --fresh
success: Switched to new orphan branch 'gh-pages'.
```

If there are uncommitted changes or untracked files, `--fresh` asks for confirmation first:

```
$ git orphan gh-pages --fresh
warning: --fresh will delete these uncommitted changes and untracked files.
 M README.md
?? notes.txt

Delete them and continue? [y/N]
> n
Aborted. Nothing was changed.
```

Create an orphan branch interactively:

```
$ git orphan
Branch name:
> gh-pages
success: Switched to new orphan branch 'gh-pages'.
```

## See also

- [`git br`](./git-br.md): Branch from current position, switch to it, and push upstream.
- [git-checkout `--orphan`](https://git-scm.com/docs/git-checkout#Documentation/git-checkout.txt---orphanltnew-branchgt)
