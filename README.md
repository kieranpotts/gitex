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

- [**Requirements**](./docs/requirements.adoc)
- [**Installation**](./docs/installation.adoc)
- [**Usage**](./docs/usage/README.adoc)
  - [`gitex`](./docs/usage/gitex.adoc)
  - [`git amend`](./docs/usage/git-amend.adoc)
  - [`git author`](./docs/usage/git-author.adoc)
  - [`git backup`](./docs/usage/git-backup.adoc)
  - [`git br`](./docs/usage/git-br.adoc)
  - [`git branches`](./docs/usage/git-branches.adoc)
  - [`git changes`](./docs/usage/git-changes.adoc)
  - [`git cl`](./docs/usage/git-cl.adoc)
  - [`git cm`](./docs/usage/git-cm.adoc)
  - [`git co`](./docs/usage/git-co.adoc)
  - [`git configure`](./docs/usage/git-configure.adoc)
  - [`git contrib`](./docs/usage/git-contrib.adoc)
  - [`git current`](./docs/usage/git-current.adoc)
  - [`git default`](./docs/usage/git-default.adoc)
  - [`git delete`](./docs/usage/git-delete.adoc)
  - [`git discard`](./docs/usage/git-discard.adoc)
  - [`git down`](./docs/usage/git-down.adoc)
  - [`git download`](./docs/usage/git-download.adoc)
  - [`git fell`](./docs/usage/git-fell.adoc)
  - [`git fetched`](./docs/usage/git-fetched.adoc)
  - [`git ff`](./docs/usage/git-ff.adoc)
  - [`git filelog`](./docs/usage/git-filelog.adoc)
  - [`git fixup`](./docs/usage/git-fixup.adoc)
  - [`git graph`](./docs/usage/git-graph.adoc)
  - [`git history`](./docs/usage/git-history.adoc)
  - [`git ignore`](./docs/usage/git-ignore.adoc)
  - [`git ignored`](./docs/usage/git-ignored.adoc)
  - [`git last`](./docs/usage/git-last.adoc)
  - [`git orphan`](./docs/usage/git-orphan.adoc)
  - [`git pick`](./docs/usage/git-pick.adoc)
  - [`git push-all`](./docs/usage/git-push-all.adoc)
  - [`git rebase-all`](./docs/usage/git-rebase-all.adoc)
  - [`git recent`](./docs/usage/git-recent.adoc)
  - [`git remotes`](./docs/usage/git-remotes.adoc)
  - [`git resume`](./docs/usage/git-resume.adoc)
  - [`git reword`](./docs/usage/git-reword.adoc)
  - [`git squash`](./docs/usage/git-squash.adoc)
  - [`git staged`](./docs/usage/git-staged.adoc)
  - [`git stashed`](./docs/usage/git-stashed.adoc)
  - [`git state`](./docs/usage/git-state.adoc)
  - [`git sw`](./docs/usage/git-sw.adoc)
  - [`git sync`](./docs/usage/git-sync.adoc)
  - [`git tags`](./docs/usage/git-tags.adoc)
  - [`git track`](./docs/usage/git-track.adoc)
  - [`git tracking`](./docs/usage/git-tracking.adoc)
  - [`git unamend`](./docs/usage/git-unamend.adoc)
  - [`git uncommit`](./docs/usage/git-uncommit.adoc)
  - [`git undo`](./docs/usage/git-undo.adoc)
  - [`git unignore`](./docs/usage/git-unignore.adoc)
  - [`git unstage`](./docs/usage/git-unstage.adoc)
  - [`git untrack`](./docs/usage/git-untrack.adoc)
  - [`git up`](./docs/usage/git-up.adoc)
  - [`git upstream`](./docs/usage/git-upstream.adoc)
  - [`git versions`](./docs/usage/git-versions.adoc)
  - [`git whoami`](./docs/usage/git-whoami.adoc)
  - [`git wip`](./docs/usage/git-wip.adoc)
  - [`git working`](./docs/usage/git-working.adoc)

### Development and maintenance

- [**Runtime tests**](./docs/runtime-tests.adoc)
- [**Static analysis**](./docs/static-analysis.adoc)

---

Copyright © 2020-present Kieran Potts, [MIT license](./LICENSE.txt)
