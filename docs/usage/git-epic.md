# `git epic`

Start a long-lived epic branch, cut from the tip of the delivery pipeline's development trunk, and checked out in a new worktree of its own.

An epic branch carries a large body of work that takes a long time, or that several people work on together, eg. a rewrite of a subsystem. It is named `[<pipeline>/]epic/[<id>-]<slug>`, eg. `latest/epic/billing-v2-rewrite`. Unlike a temp branch, an epic branch is shared, so its history is never rewritten. While the work goes on, the development trunk is merged into the epic to keep it current. When the work is done, the epic is squashed into the development trunk as a single commit. [`git integrate`](./git-integrate.md) does both. For a small piece of work owned by one person, use [`git temp`](./git-temp.md) instead.

The command works like this:

1. It brings the development trunk, `[<pipeline>/]dev`, up to date with the remote. Where a worktree has the trunk checked out, the trunk is fast-forwarded there, but only if that worktree is clean. Where no worktree has it, the local branch is fast-forwarded with `git fetch origin dev:dev`. Either way, only a fast-forward is allowed. If the local trunk has diverged from the remote, the command stops.

2. It checks that the new branch name is free, both locally and on the remote, and that nothing exists yet at the new worktree's path.

3. It creates the branch at the tip of the development trunk, checked out in a new worktree beside the others, named after the branch with each `/` replaced by `-`, eg. `<project>/latest-epic-billing-v2-rewrite`.

The current worktree is never touched, so it may be dirty. No worktree is switched to another branch, and nothing is committed or pushed. Because an epic is shared, you will usually want to push it straight away, with the command printed on the last line of the output.

## Usage

```
$ git epic <slug> [--id <id>] [--pipeline <name>] [--no-color]
```

The `<slug>` is a short description of the work, eg. `billing-v2-rewrite`. It may hold only lowercase letters, digits, and hyphens, and it must start and end with a letter or a digit. It must not be longer than 72 characters. A slug longer than 50 characters is allowed, but prints a warning.

Options:

- `--id <id>` \
  Prefix the slug with an issue number or other tracking identifier. The identifier is copied verbatim, including its letter case, eg. `--id PRD-187` gives `PRD-187-<slug>`.

- `--pipeline <name>` \
  Cut the branch in the named delivery pipeline, eg. `v1`, instead of the one determined from the current branch. The name is copied verbatim, eg. `v2.4-LTS`.

- `--no-color` \
  Disable colored output. See [Colored output](../configuration.md#colored-output).

- `--help`, `-h` \
  Show usage instructions.

## Requirements

`git epic` works only in a repository laid out for the pipeline workflow.

- The repository is a bare clone in a directory named `.bare`, with each worktree checked out in a directory beside it, eg. `acme/.bare` and `acme/default`.

- The branches follow a trunk-based model (see [TS-9](https://kieranpotts.com/standards/009)). Each delivery pipeline has a development trunk, `dev`, from which short-lived `temp/*` and long-lived `epic/*` branches are cut. Every branch in a pipeline carries the pipeline's name as a prefix, eg. `latest/dev` or `v1/epic/auth-overhaul`. A project with a single, perpetual pipeline may leave the pipeline unnamed, eg. `dev` or `epic/auth-overhaul`.

Unless `--pipeline` is given, the pipeline is read from the branch checked out in the current worktree: `latest/dev` gives `latest`, `v1/temp/42-fix-auth` gives `v1`, and `dev` gives the unnamed pipeline. Where the current worktree's `HEAD` is detached, the branch checked out in the `default` worktree is used instead.

The command fetches from the `origin` remote, or from the remote named by [`GITEX_DEFAULT_REMOTE_NAME`](../configuration.md#gitex_default_remote_name). If the repository has no such remote, the command warns, skips the fetch, and works from local refs.

The command stops, and changes nothing, in any of these cases:

- The repository is not laid out as described above.
- The slug or the identifier is invalid, or the full branch name is not a valid Git ref.
- The pipeline cannot be determined, eg. the current branch is `main`, and `--pipeline` is not given.
- The pipeline has no development trunk, eg. there is no `v2/dev`.
- The development trunk's worktree has uncommitted changes, or a merge in progress.
- The local development trunk has diverged from the remote.
- The branch name is already taken, locally or on the remote. Choose a more specific slug.
- A file or directory already exists at the new worktree's path.

## Output

The first two lines of stdout are fixed, so that a script can read them.

1. The new branch name.
2. The absolute path of the new worktree.

These are followed by the commit the branch was cut from, and the command to publish the branch. Warnings and errors go to stderr.

## Exit status

- `0`: The branch and its worktree were created.
- `1`: An error, or a refusal for one of the reasons listed above. Nothing was changed, except that the development trunk may have been fast-forwarded.

## Examples

Start an epic branch, from a worktree in the "latest" pipeline:

```
$ git epic billing-v2-rewrite
latest/epic/billing-v2-rewrite
/home/me/dev/acme/latest-epic-billing-v2-rewrite
Cut from latest/dev at 3f9c2ab.
To publish: git push --set-upstream origin latest/epic/billing-v2-rewrite
```

Start an epic branch with a tracking identifier, in the "v1" pipeline:

```
$ git epic auth-overhaul --id PRD-187 --pipeline v1
v1/epic/PRD-187-auth-overhaul
/home/me/dev/acme/v1-epic-PRD-187-auth-overhaul
Cut from v1/dev at 81d4a07.
To publish: git push --set-upstream origin v1/epic/PRD-187-auth-overhaul
```

## See also

- [`git temp`](./git-temp.md) \
  Start a short-lived temp branch, in a worktree of its own.

- [`git integrate`](./git-integrate.md) \
  Merge the development trunk into the epic, or squash the epic into the development trunk.
