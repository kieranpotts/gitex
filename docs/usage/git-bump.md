# `git bump`

Work out the next semantic version from the commits made since the last release, promote the changelog's "unreleased" section to that version, update the version manifests, and commit the lot as `version: <version>`.

The command works like this:

1. It finds the release baseline: the most recent release tag of the pipeline that is reachable from `HEAD`. Release tags take the form `v<major>.<minor>.<patch>`. Pre-release tags, eg. `v1.5.0-rc.0`, are never a baseline. Where the pipeline is named after a version series, eg. `v1` or `v2.4-LTS`, only tags in that series count, eg. `v1.*` or `v2.4.*`.

2. It gathers the commits made since the baseline, leaving out merge commits, and commits that touch only the changelog.

3. It works out the bump that each commit calls for, from the type and flag in its subject (see [How commits are classified](#how-commits-are-classified)), and takes the highest. A major bump beats a minor bump, which beats a patch bump.

4. It applies the bump to the baseline version. A major bump takes `1.4.2` to `2.0.0`, a minor bump to `1.5.0`, and a patch bump to `1.4.3`.

5. It promotes the changelog, and sets the new version in each version manifest (see [Changelog](#changelog) and [Version manifests](#version-manifests)).

6. It commits the changelog and the manifests, and no other file, with the message `version: <version>`. Your commit hooks run as usual.

The version comes from the commit history alone. Each commit's author stated its type and flags, and the bump follows from those, not from the diffs.

`git bump` never creates, moves, or deletes a tag, and it never pushes. Once the version commit has passed through the pipeline, tag it with [`git release`](./git-release.md).

## Usage

```
$ git bump [--pre <stage>] [--dry-run] [--no-color]
```

Run the command in the worktree of the development trunk, or of a temp or epic branch. The version commit is made on the branch checked out there.

Options:

- `--pre <stage>` \
  Make a pre-release, eg. `--pre rc` gives `1.5.0-rc.0`. The stage may hold only lowercase letters, eg. `alpha`, `beta`, or `rc`. The counter is one more than the highest existing tag for that version and stage, or `0` where there is none, eg. if `v1.5.0-rc.1` exists, the next is `1.5.0-rc.2`. See [Pre-releases](#pre-releases).

- `--dry-run` \
  Print the next version and the commits that decided it, but change nothing. Every check still runs, so a script can use this to find out whether a real run would succeed.

- `--no-color` \
  Disable colored output. See [Colored output](../configuration.md#colored-output).

- `--help`, `-h` \
  Show usage instructions.

## How commits are classified

The type is read from the subject's `<type>:` prefix, and any flag from its ` - <FLAG>` suffix.

| Commit                                      | Bump  |
| ------------------------------------------- | ----- |
| Any type, flagged `BREAKING`                | Major |
| `behavior`, `fix`, `quality`                | Minor |
| `maintenance`, `refactor`, `style`, `chore` | Patch |
| `create`, `update`, `delete`                | Patch |
| `step`, `version`, `revert`                 | None  |

There are some special cases.

- `INCOMPAT` marks a breaking change that consumers cannot see, so it never calls for a major bump. The commit is classified by its type.

- A `revert:` commit names the commit it reverts in a `Reverts: <hash>` footer. If both commits are in the range, both are left out, because the change never reaches a consumer.

- A commit with no recognized type is counted as a minor bump, the safer error, and named in a warning, so that you can check it.

- While the baseline version is `0.x.y`, a `BREAKING` commit calls for a minor bump, not a major one. Version zero makes no compatibility promise, and moving to `1.0.0` is a decision for a human. A warning says when a breaking change was absorbed this way.

If no commit calls for a bump, there is nothing to release. The command prints the current version, and exits with status `2`.

## Changelog

`git bump` supports changelogs in the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format only.

- The changelog is `CHANGELOG.md` at the root of the repository, unless the [`GITEX_CHANGELOG`](../configuration.md#gitex_changelog) environment variable names another path, relative to the root.

- The "unreleased" section starts at the line `## [Unreleased]`, and runs to the next `## ` heading or to the end of the file. The section is empty if it holds only blank lines.

- A released section's heading takes the form `## [<version>] - <YYYY-MM-DD>`.

To promote the changelog, the command renames `## [Unreleased]` to `## [<version>] - <today>`, and inserts a new, empty `## [Unreleased]` section above it. No entry is added, reworded, reordered, or removed. Every other line, including any link reference definitions at the foot of the file, stays exactly as it was.

If the project has no changelog file, the promotion is skipped.

## Version manifests

`git bump` looks for these version manifests, at the root of the repository only:

| Manifest         | Field                                                        |
| ---------------- | ------------------------------------------------------------ |
| `package.json`   | `"version": "<value>"`                                       |
| `pyproject.toml` | `version = "<value>"`, in the `[project]` or `[tool.poetry]` table |
| `Cargo.toml`     | `version = "<value>"`, in the `[package]` table              |

The manifests are edited line by line, without a JSON or TOML parser.

- In each manifest, exactly one line must match the field. If no line matches, or several do, the command names the manifest and stops, rather than guess. In the TOML manifests, only lines in the named table count, so a `version = "1.0"` line in a `[dependencies.serde]` table is ignored.

- Only the quoted value changes. Every other byte of the file stays the same, including the rest of the matched line.

- Every manifest is checked before any file is written, so a refusal never leaves a half-finished edit behind.

Lockfiles, such as `package-lock.json`, `poetry.lock`, and `Cargo.lock`, are never edited. Regenerate them with your package manager if they record the version.

A project whose version is not held in one of these fields cannot use `git bump`, eg. one with a dynamic version in `pyproject.toml`, a Cargo workspace member with `version.workspace = true`, or a manifest in a subdirectory.

If the project has neither a changelog nor a manifest, there is nothing to commit. The command prints the version, and makes no commit.

## Pre-releases

With `--pre`, the version is worked out as usual, and then the pre-release suffix is added, eg. `1.5.0-rc.0`.

A pre-release sets the version in the manifests, but leaves the changelog as it is. The entries stay in the "unreleased" section until the final release, `1.5.0`, promotes them. A pre-release therefore needs at least one version manifest. Without one, there would be nothing to commit, so the command stops.

## First release

If the pipeline has no release tags at all, this is its first release. All commits from the root of the history count, and the version is `1.0.0`, unless the [`GITEX_INITIAL_VERSION`](../configuration.md#gitex_initial_version) environment variable gives another, eg. `0.1.0`.

If the changelog already has a released section, though no tag exists for any release, the command stops and reports the missing tag. It does not treat the whole history as unreleased.

## Requirements

`git bump` works only in a repository laid out for the pipeline workflow.

- The repository is a bare clone in a directory named `.bare`, with each worktree checked out in a directory beside it, eg. `acme/.bare` and `acme/default`.

- The branches follow a trunk-based model (see [TS-9](https://kieranpotts.com/standards/009)). Each delivery pipeline has a development trunk, `dev`, an optional `test` trunk, a release-ready trunk, `ready`, and a `release` trunk, plus short-lived `temp/*` and long-lived `epic/*` branches. Every branch in a pipeline carries the pipeline's name as a prefix, eg. `latest/dev` or `v1/temp/42-fix-auth`. A project with a single, perpetual pipeline may leave the pipeline unnamed, eg. `dev` or `temp/42-fix-auth`.

- Commit subjects take the form `<type>: <description>[ - <FLAG>]`, eg. `fix: escape apostrophes in search query` or `behavior: return 429 when rate limited - BREAKING`.

- Release tags take the form `v<major>.<minor>.<patch>`, with an optional `-<stage>.<n>` pre-release suffix.

The pipeline is read from the branch checked out in the current worktree: `latest/dev` gives `latest`, `v1/temp/42-fix-auth` gives `v1`, and `dev` gives the unnamed pipeline.

The command fetches tags from the `origin` remote, or from the remote named by [`GITEX_DEFAULT_REMOTE_NAME`](../configuration.md#gitex_default_remote_name). If the repository has no such remote, the command warns, skips the fetch, and works from local tags.

The command stops, and changes nothing, in any of these cases:

- The repository is not laid out as described above.
- The current worktree's `HEAD` is detached, or the branch checked out is a `test`, `ready`, or `release` trunk. Those trunks only ever move by fast-forward.
- The current worktree has uncommitted changes, or a merge, rebase, cherry-pick, revert, or squash in progress.
- The project's tags follow some other scheme, eg. calendar versioning.
- The bump would take the version outside the pipeline's series, eg. a major bump in the `v1` pipeline, or a minor bump in the `v2.4-LTS` pipeline. Only a human can decide whether to drop the change or release it from another pipeline.
- A tag already exists for the new version.
- The changelog's "unreleased" section is missing or empty. Bring the changelog up to date first.
- The changelog is not in the Keep a Changelog format.
- A manifest's version field matches no line, or several.
- The changelog has a released section, but the pipeline has no release tags.
- `--pre` is given, and the project has no version manifest.

If a commit hook rejects the version commit, the command stops, and leaves the edits to the changelog and manifests uncommitted, so that you can fix the problem and commit them yourself. To start again instead, discard them with `git restore`.

## Output

The first line of stdout is the new version, bare, with no `v` prefix, eg. `1.5.0`, so that a script can read it.

It is followed by the baseline tag, the bump level, the commits that decided the bump, by short hash and subject, and the version commit. Warnings, eg. about commits with no recognized type, and errors go to stderr.

When there is nothing to release, the first line is the current version. If the pipeline has never released, stdout is empty.

## Exit status

- `0`: The version commit was made, or, with `--dry-run` or in a project with neither changelog nor manifest, the next version was printed.
- `1`: An error, or a refusal for one of the reasons listed above.
- `2`: Nothing to do. No commit since the baseline calls for a bump.

## Examples

Bump the version, where the commits since `v1.4.2` include a feature and a fix:

```
$ git bump
1.5.0
Baseline: v1.4.2
Bump: minor
Decided by:
  9c1d2e3 behavior: add format option to export
  4a5b6c7 fix: escape apostrophes in search query
Committed 7e8f9a0 (version: 1.5.0), changing CHANGELOG.md and package.json.
```

In `CHANGELOG.md`, the heading `## [Unreleased]` became `## [1.5.0] - 2026-11-24`, under a new, empty `## [Unreleased]` section.

See what the next version would be, without changing anything:

```
$ git bump --dry-run
2.0.0
Baseline: v1.4.2
Bump: major
Decided by:
  b2c3d4e behavior: return 429, not 503, when rate limited - BREAKING
```

Make the next release candidate:

```
$ git bump --pre rc
1.5.0-rc.2
Baseline: v1.4.2
Bump: minor
Decided by:
  9c1d2e3 behavior: add format option to export
Committed 1f2e3d4 (version: 1.5.0-rc.2), changing package.json.
```

Nothing has changed that calls for a release:

```
$ git bump
1.4.2
Nothing to release since v1.4.2.
```

The changelog has not been brought up to date:

```
$ git bump
error: The "unreleased" section of CHANGELOG.md is empty.
Add entries for the changes since v1.4.2, then run git bump again.
```

## See also

- [`git release`](./git-release.md) \
  Tag the version commit, and promote it to the release trunks.

- [`git versions`](./git-versions.md) \
  List the version tags, sorted numerically.
