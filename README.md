# GitEx ![Integration tests passing](https://img.shields.io/github/actions/workflow/status/kieranpotts/gitex/integration.yaml?branch=dev&style=flat-square&label=tests&labelColor=%23333333&color=%23008800&cacheSeconds=86400)

GitEx is a suite of useful Git extensions – things like `git sync`, `git amend`, `git squash`, `git fixup`, and `git undo`.

> [!IMPORTANT]
> This project is a **work-in-progress** and is not intended for production use at this time.

The extensions are intended to offer a slightly higher level of abstraction for working with Git at the command line. However, GitEx does not oppose any opinions on concerns such as branch naming and committing conventions. GitEx only extends Git's built-in suite of general-purpose commands.

The extensions are implemented as POSIX-compliant Unix shell scripts. To install the extensions, all you need to do is add the scripts to your operating system's `PATH` environment variable. Git will automatically integrate the scripts as [Git aliases](https://git-scm.com/book/ms/v2/Git-Basics-Git-Aliases).

GitEx is inspired by TJ Holowaychuk's [Git Extras](https://github.com/tj/git-extras). But GitEx is not a fork and it is not designed to be compatible with, or a drop-in replacement for, Git Extras. Although some GitEx extensions have similar APIs to those in Git Extras, their behaviors are different. For this reason, it is not recommended to try to install both GitEx and Git Extras side-by-side – you should choose one or the other.

> [!WARNING]
> You use these Git extensions at your own risk. Some operations enabled via these extensions are potentially destructive. For example, some of the extensions will rewrite the commit histories of your Git repositories.

## Documentation

### Usage

- [**Requirements**](./docs/requirements.md)
- [**Installation**](./docs/installation.md)
- [**Usage**](./docs/usage/README.md)
  - [`gitex`](./docs/usage/gitex.md)
  - [`git amend`](./docs/usage/git-amend.md)
  - [`git author`](./docs/usage/git-author.md)
  - [`git backup`](./docs/usage/git-backup.md)
  - [`git br`](./docs/usage/git-br.md)
  - [`git branches`](./docs/usage/git-branches.md)
  - [`git changes`](./docs/usage/git-changes.md)
  - [`git cl`](./docs/usage/git-cl.md)
  - [`git cm`](./docs/usage/git-cm.md)
  - [`git co`](./docs/usage/git-co.md)
  - [`git configure`](./docs/usage/git-configure.md)
  - [`git contrib`](./docs/usage/git-contrib.md)
  - [`git current`](./docs/usage/git-current.md)
  - [`git default`](./docs/usage/git-default.md)
  - [`git delete`](./docs/usage/git-delete.md)
  - [`git discard`](./docs/usage/git-discard.md)
  - [`git down`](./docs/usage/git-down.md)
  - [`git download`](./docs/usage/git-download.md)
  - [`git fell`](./docs/usage/git-fell.md)
  - [`git fetched`](./docs/usage/git-fetched.md)
  - [`git ff`](./docs/usage/git-ff.md)
  - [`git filelog`](./docs/usage/git-filelog.md)
  - [`git fixup`](./docs/usage/git-fixup.md)
  - [`git graph`](./docs/usage/git-graph.md)
  - [`git history`](./docs/usage/git-history.md)
  - [`git ignore`](./docs/usage/git-ignore.md)
  - [`git ignored`](./docs/usage/git-ignored.md)
  - [`git last`](./docs/usage/git-last.md)
  - [`git orphan`](./docs/usage/git-orphan.md)
  - [`git pick`](./docs/usage/git-pick.md)
  - [`git push-all`](./docs/usage/git-push-all.md)
  - [`git rebase-all`](./docs/usage/git-rebase-all.md)
  - [`git recent`](./docs/usage/git-recent.md)
  - [`git remotes`](./docs/usage/git-remotes.md)
  - [`git resume`](./docs/usage/git-resume.md)
  - [`git reword`](./docs/usage/git-reword.md)
  - [`git squash`](./docs/usage/git-squash.md)
  - [`git staged`](./docs/usage/git-staged.md)
  - [`git stashed`](./docs/usage/git-stashed.md)
  - [`git state`](./docs/usage/git-state.md)
  - [`git sw`](./docs/usage/git-sw.md)
  - [`git sync`](./docs/usage/git-sync.md)
  - [`git tags`](./docs/usage/git-tags.md)
  - [`git track`](./docs/usage/git-track.md)
  - [`git tracking`](./docs/usage/git-tracking.md)
  - [`git unamend`](./docs/usage/git-unamend.md)
  - [`git uncommit`](./docs/usage/git-uncommit.md)
  - [`git undo`](./docs/usage/git-undo.md)
  - [`git unignore`](./docs/usage/git-unignore.md)
  - [`git unstage`](./docs/usage/git-unstage.md)
  - [`git untrack`](./docs/usage/git-untrack.md)
  - [`git up`](./docs/usage/git-up.md)
  - [`git upstream`](./docs/usage/git-upstream.md)
  - [`git versions`](./docs/usage/git-versions.md)
  - [`git whoami`](./docs/usage/git-whoami.md)
  - [`git wip`](./docs/usage/git-wip.md)
  - [`git working`](./docs/usage/git-working.md)

### Development and maintenance

- [**Runtime tests**](./docs/runtime-tests.md)
- [**Static analysis**](./docs/static-analysis.md)

-----

Copyright © 2020-present Kieran Potts, [MIT license](./LICENSE.txt)
