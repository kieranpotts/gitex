# `git integrate`

Integrate the checked-out branch into another branch of the same delivery pipeline, using the strategy that the pair of branches calls for, and working on the target in its own worktree.

The branch checked out in the current worktree is the source. The target is the branch the work lands on. The strategy depends on what kind of branch each one is:

| Source                    | Target                 | Strategy                  |
| ------------------------- | ---------------------- | ------------------------- |
| `[<pipeline>/]temp/*`     | `[<pipeline>/]dev`     | Rebase, then fast-forward |
| `[<pipeline>/]epic/*`     | `[<pipeline>/]dev`     | Merge down, then squash   |
| `[<pipeline>/]dev`        | `[<pipeline>/]epic/*`  | Merge commit              |
| `[<pipeline>/]dev`        | `[<pipeline>/]test`    | Fast-forward              |
| `[<pipeline>/]test`       | `[<pipeline>/]ready`   | Fast-forward              |
| `[<pipeline>/]dev`        | `[<pipeline>/]ready`   | Fast-forward              |
| `[<pipeline>/]ready`      | `[<pipeline>/]release` | Fast-forward              |

Any other pair is refused. The development trunk is promoted straight to `ready` only where the pipeline has no `test` trunk. One run moves one row of the table, so a promotion from `dev` to `release` takes three runs. To tag a release and promote it to `ready` and `release` in one step, use [`git release`](./git-release.md) instead.

Each strategy works like this:

- **Rebase, then fast-forward.** The temp branch is rebased onto the development trunk, in the current worktree. Then the trunk is fast-forwarded to it, in the trunk's worktree. The temp branch's commits land on the trunk one by one, with no merge commit, so each one can be reverted on its own.

- **Merge down, then squash.** The development trunk is first merged into the epic, in the current worktree, with the message `merge: sync with <target>`. That way the epic resolves any divergence itself. Then the epic is squash-merged into the trunk, in the trunk's worktree, as a single commit.

- **Merge commit.** The development trunk is merged into the epic, in the epic's worktree, with the message `merge: sync with <source>`.

- **Fast-forward.** The target trunk is fast-forwarded to the source trunk, in the target's worktree. If that is not possible, the target carries a commit that the source does not. Every change must reach a trunk from `dev`, so the command stops and reports this rather than work around it.

Before it integrates anything, the command brings each shared branch involved, ie. each trunk and epic, up to date with the remote, by fast-forward only. A temp branch is personal, so its local copy is taken as it is.

If Git stops on a conflict, the command never resolves it. It lists the conflicted paths, aborts the rebase or merge, and stops. Both branches are left as they were before the run.

The command never switches the branch checked out in any worktree, and it changes a worktree only after finding it clean. It never uses `--no-verify`, `--allow-empty`, `-X ours`, or `-X theirs`. It never pushes, and it never deletes a branch or a worktree. When the work is integrated, it prints the command that would publish it.

> [!CAUTION]
> Integrating a temp branch rebases it, which rewrites its history. If you have already pushed the temp branch, its remote copy will no longer match, and you will need to force-push or delete it. The history of a trunk or an epic branch is never rewritten.

## Usage

```
$ git integrate [<target>] [-m <description>] [--no-color]
```

The `<target>` defaults to the pipeline's development trunk, `[<pipeline>/]dev`, when the source is a temp or epic branch. When the source is a trunk, the target must be given. You may give the target with or without the pipeline's prefix, eg. `test` or `latest/test`.

Where no worktree has the target checked out, one is created beside the others, named after the branch with each `/` replaced by `-`, eg. `<project>/latest-test`.

Options:

- `-m <description>` \
  The description of the epic's outcome, for the squash commit. Required when integrating an epic into the development trunk, and refused otherwise. See [The squash commit](#the-squash-commit).

- `--no-color` \
  Disable colored output. See [Colored output](../configuration.md#colored-output).

- `--help`, `-h` \
  Show usage instructions.

## The squash commit

When an epic is squashed into the development trunk, the commit message is computed from the epic's own commits, ie. the non-merge commits reachable from the epic but not from the trunk. Only the description comes from you, via `-m`.

```
<type>: <description>[ - <flag>]

- <subject of the epic's first commit>
- <subject of the epic's second commit>
- …
```

- The `<type>` is the type with the most impact among the epic's commits, in this order: `behavior`, `fix`, `quality`, `maintenance`, `step`, `refactor`, `style`, `chore`. Commits of any other type, or with no type, do not count. If no commit has one of these types, the command stops.

- The `<flag>` is `BREAKING` if any of the epic's commits carries it, or else `INCOMPAT` if any carries that. The flags `WIP`, `TEMPORARY`, and `EXPERIMENT` describe intermediate states that the squash erases, so they are dropped.

- The body lists the subjects of the epic's commits, oldest first, one per line.

The subject must not be longer than 72 characters, or the command stops before it changes anything. A subject longer than 50 characters is allowed, but prints a warning.

The commit runs your commit hooks. If a hook rejects the message, the squash is undone with `git reset --merge`, the trunk is left where it was, and the command stops. The epic keeps its merge-down commit, which is an ordinary merge of the trunk, and you can run the command again once the problem is fixed.

## Requirements

`git integrate` works only in a repository laid out for the pipeline workflow.

- The repository is a bare clone in a directory named `.bare`, with each worktree checked out in a directory beside it, eg. `acme/.bare` and `acme/default`.

- The branches follow a trunk-based model (see [TS-9](https://kieranpotts.com/standards/009)). Each delivery pipeline has a development trunk, `dev`, an optional `test` trunk, a release-ready trunk, `ready`, and a `release` trunk, plus short-lived `temp/*` and long-lived `epic/*` branches. Every branch in a pipeline carries the pipeline's name as a prefix, eg. `latest/dev` or `v1/temp/42-fix-auth`. A project with a single, perpetual pipeline may leave the pipeline unnamed, eg. `dev` or `temp/42-fix-auth`.

- Commit subjects take the form `<type>: <description>[ - <FLAG>]`, eg. `fix: escape apostrophes in search query` or `behavior: return 429 when rate limited - BREAKING`.

The pipeline is read from the source branch: `latest/dev` gives `latest`, `v1/temp/42-fix-auth` gives `v1`, and `dev` gives the unnamed pipeline.

The command fetches from the `origin` remote, or from the remote named by [`GITEX_DEFAULT_REMOTE_NAME`](../configuration.md#gitex_default_remote_name). If the repository has no such remote, the command warns, skips the fetch, and works from local refs.

The command stops, and changes nothing, in any of these cases:

- The repository is not laid out as described above.
- The current worktree's `HEAD` is detached, so there is no source branch.
- The current worktree or the target's worktree has uncommitted changes, or a merge, rebase, or squash in progress.
- The source is a trunk, and no target is given.
- The pair of branches is not in the table above, eg. `dev` into `ready` in a pipeline that has a `test` trunk.
- The target is in another pipeline, eg. `latest/temp/42-fix-auth` into `v2/dev`. That is a backport, which calls for a cherry-pick.
- A temp branch carries a commit flagged `WIP` or `TEMPORARY`. A broken build, or a commit meant to be reverted, must not reach the trunk.
- A shared branch has diverged from its copy on the remote.
- `-m` is missing when integrating an epic, or given for any other pair.
- The squash commit's subject would be longer than 72 characters.
- A fast-forward is not possible.

## Output

The first three lines of stdout are fixed, so that a script can read them.

1. The target branch and its new short hash, eg. `latest/dev 3f9c2ab`.
2. The absolute path of the target's worktree.
3. The strategy used: `rebase-and-fast-forward`, `merge-down-and-squash`, `merge-commit`, or `fast-forward`.

These are followed by the command to publish the integrated branches.

When the source is already integrated, the first two lines describe the target as it stands, and the strategy line is omitted.

When the run stops on a conflict, stdout holds only the conflicted paths, one per line.

Warnings and errors go to stderr.

## Exit status

- `0`: The source was integrated into the target.
- `1`: An error, a refusal, or a conflict. Both branches are left as they were before the run, except that an epic may keep its merge-down commit.
- `2`: Nothing to do. The source is already an ancestor of the target.

## Examples

Integrate a temp branch into the development trunk, from the temp branch's worktree:

```
$ git integrate
latest/dev 3f9c2ab
/home/me/dev/acme/default
rebase-and-fast-forward
To publish: git push origin latest/dev
```

Squash an epic into the development trunk:

```
$ git integrate -m "rewrite billing engine"
latest/dev 9b4e1f2
/home/me/dev/acme/default
merge-down-and-squash
To publish: git push origin latest/dev latest/epic/billing-v2-rewrite
```

The squash commit's message is computed from the epic's commits:

```
behavior: rewrite billing engine - BREAKING

- step: extract invoice model
- behavior: replace legacy tax rules - BREAKING
- fix: round line totals to the currency's minor unit
```

Merge the development trunk into an epic, from the trunk's worktree:

```
$ git integrate latest/epic/billing-v2-rewrite
latest/epic/billing-v2-rewrite 5c7d8e9
/home/me/dev/acme/latest-epic-billing-v2-rewrite
merge-commit
To publish: git push origin latest/epic/billing-v2-rewrite
```

Promote the development trunk to the `test` trunk:

```
$ git integrate test
latest/test 3f9c2ab
/home/me/dev/acme/latest-test
fast-forward
To publish: git push origin latest/test
```

The merge-down stops on a conflict:

```
$ git integrate -m "rewrite billing engine"
src/billing/invoice.ts
error: Merging latest/dev into latest/epic/billing-v2-rewrite stopped on a conflict.
Resolve the conflict by merging latest/dev into the epic yourself, then run git integrate again.
```

The target carries a commit that the source does not:

```
$ git integrate test
error: latest/test cannot be fast-forwarded to latest/dev.
latest/test carries a commit that is not on latest/dev. Every change must reach a trunk from dev.
```

## See also

- [`git temp`](./git-temp.md) \
  Start a short-lived temp branch, in a worktree of its own.

- [`git epic`](./git-epic.md) \
  Start a long-lived epic branch, in a worktree of its own.

- [`git release`](./git-release.md) \
  Tag a version commit, and promote it to the release trunks.

- [`git squash`](./git-squash.md) \
  Perform a squash merge, in any repository.
