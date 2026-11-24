# `git release`

Release a version, by tagging its version commit, fast-forwarding the release-ready trunk to the tag, and fast-forwarding the release trunk to match, each in its own worktree.

After a release, the tag `v<version>`, the `[<pipeline>/]ready` trunk, and the `[<pipeline>/]release` trunk all point at the same commit: the one whose subject is `version: <version>`. [`git bump`](./git-bump.md) makes that commit.

The command works like this:

1. It brings the source trunk, `[<pipeline>/]ready`, and `[<pipeline>/]release` up to date with the remote, by fast-forward only. The source trunk is `[<pipeline>/]test` where the pipeline has one, or else `[<pipeline>/]dev`.

2. It finds the version commit on the source trunk. There must be exactly one commit whose subject is `version: <version>`.

3. It checks that `ready` and `release` are at or behind the version commit. The commits after the version commit on the source trunk belong to a later release, so `ready` is never moved past it.

4. It creates an annotated tag, `v<version>`, on the version commit, with the message `Release <version>`. Where `tag.gpgSign` or `commit.gpgSign` is `true` in your Git configuration, the tag is signed.

5. It fast-forwards `ready` to the tag, then `release` to `ready`, each in its own worktree. Where no worktree has one of them checked out, a worktree is created beside the others, named after the branch with each `/` replaced by `-`, eg. `<project>/latest-ready`. Where the pipeline has no `release` trunk yet, this is its first release, and the trunk is created at `ready`, in a new worktree.

A pre-release, eg. `1.3.0-rc.0`, is tagged, but `ready` and `release` stay where they are. A pre-release is for testing, not for production.

The command can pick up where an earlier run stopped. If the tag already points at the version commit, it is left as it is, and the trunks are moved as usual.

`git release` only ever fast-forwards `ready` and `release`. It never merges, resets, or force-moves them. It never switches the branch checked out in any worktree, and it moves a branch in its worktree only after finding that worktree clean. It makes no commits, and it never pushes. Publishing the tag and the trunks usually triggers a deployment, so that is left to you. The command prints the push command to run.

> [!IMPORTANT]
> Release tags are permanent. `git release` never moves, deletes, or recreates a tag. If the tag already exists on some other commit, the command stops.

## Usage

```
$ git release <version> [--pipeline <name>] [--no-color]
```

The `<version>` is a semantic version, of the form `<major>.<minor>.<patch>`, with an optional `-<stage>.<n>` pre-release suffix, eg. `1.2.0` or `1.3.0-rc.0`. A leading `v` is dropped, so `v1.2.0` means the same as `1.2.0`. The command never works out the version itself.

Options:

- `--pipeline <name>` \
  Release from the named delivery pipeline, eg. `v1`, instead of the one determined from the current branch. The name is copied verbatim, eg. `v2.4-LTS`.

- `--no-color` \
  Disable colored output. See [Colored output](../configuration.md#colored-output).

- `--help`, `-h` \
  Show usage instructions.

## Requirements

`git release` works only in a repository laid out for the pipeline workflow.

- The repository is a bare clone in a directory named `.bare`, with each worktree checked out in a directory beside it, eg. `acme/.bare` and `acme/default`.

- The branches follow a trunk-based model (see [TS-9](https://kieranpotts.com/standards/009)). Each delivery pipeline has a development trunk, `dev`, an optional `test` trunk, a release-ready trunk, `ready`, and a `release` trunk, plus short-lived `temp/*` and long-lived `epic/*` branches. Every branch in a pipeline carries the pipeline's name as a prefix, eg. `latest/dev` or `v1/temp/42-fix-auth`. A project with a single, perpetual pipeline may leave the pipeline unnamed, eg. `dev` or `temp/42-fix-auth`.

Unless `--pipeline` is given, the pipeline is read from the branch checked out in the current worktree: `latest/dev` gives `latest`, `v1/temp/42-fix-auth` gives `v1`, and `dev` gives the unnamed pipeline. Where the current worktree's `HEAD` is detached, the branch checked out in the `default` worktree is used instead.

The command fetches branches and tags from the `origin` remote, or from the remote named by [`GITEX_DEFAULT_REMOTE_NAME`](../configuration.md#gitex_default_remote_name). If the repository has no such remote, the command warns, skips the fetch, and works from local refs.

The current worktree is never touched, so it may be dirty.

The command stops, and changes nothing, in any of these cases:

- The repository is not laid out as described above.
- The version is missing, or is not a semantic version.
- The pipeline cannot be determined, eg. the current branch is `main`, and `--pipeline` is not given.
- The pipeline has no `ready` trunk. Releases are cut only from a trunk that holds production-grade revisions.
- The worktree of `ready` or `release` has uncommitted changes, or a merge in progress.
- A local trunk has diverged from its copy on the remote.
- No commit on the source trunk has the subject `version: <version>`, or several do. The version commit has not been promoted that far yet, or was never made.
- `ready` or `release` has already moved past the version commit, so the release trunk could no longer match the tag.
- The tag already exists, on some other commit.
- A worktree cannot be created, eg. because the directory already exists.

## Output

The first line of stdout is the tag, eg. `v1.2.0`, so that a script can read it.

It is followed by the tagged commit, the worktrees moved or created, and the command to publish the release. Warnings and errors go to stderr.

## Exit status

- `0`: The release was cut, or an interrupted release was finished.
- `1`: An error, or a refusal for one of the reasons listed above.
- `2`: Nothing to do. The tag already points at the version commit, and so do `ready` and `release`.

## Examples

Release `1.2.0` in the "latest" pipeline, where `latest/test` holds the version commit:

```
$ git release 1.2.0
v1.2.0
Tagged 4b1e9d0 (version: 1.2.0).
Moved latest/ready to 4b1e9d0, in /home/me/dev/acme/latest-ready.
Moved latest/release to 4b1e9d0, in /home/me/dev/acme/latest-release.
To publish: git push origin v1.2.0 latest/ready latest/release
```

Cut the first release in the "v2" pipeline, which creates its `release` trunk:

```
$ git release 2.0.0 --pipeline v2
v2.0.0
Tagged 6a7b8c9 (version: 2.0.0).
Moved v2/ready to 6a7b8c9, in /home/me/dev/acme/v2-ready.
Created v2/release at 6a7b8c9, in /home/me/dev/acme/v2-release.
To publish: git push origin v2.0.0 v2/ready v2/release
```

Tag a release candidate, which leaves the trunks where they are:

```
$ git release 1.3.0-rc.0
v1.3.0-rc.0
Tagged 2d3e4f5 (version: 1.3.0-rc.0).
To publish: git push origin v1.3.0-rc.0
```

The version commit has not reached the source trunk yet:

```
$ git release 1.3.0
error: No commit on latest/test has the subject "version: 1.3.0".
Promote the version commit to latest/test with git integrate, then run git release again.
```

## See also

- [`git bump`](./git-bump.md) \
  Work out the next version, and make the version commit.

- [`git integrate`](./git-integrate.md) \
  Promote the version commit through the trunks.

- [`git versions`](./git-versions.md) \
  List the version tags, sorted numerically.
