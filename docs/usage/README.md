# Usage

GitEx adds the following commands to Git:

- [`gitex`](./gitex.md) — Get help with GitEx commands.

## Cloning

- [`git cl`](./git-cl.md) ✅ — Shortcut for `git clone`. Parameters are forwarded.

## Branching

- [`git br`](./git-br.md) ✅ — Branch from current position, switch to it, and push upstream to setup tracking.

- [`git orphan`](./git-orphan.md) — Create an orphaned branch and switch to it. Working changes will be added to the staging index, unless the `--fresh` option is provided, in which case the working directory will be cleared – careful, you may lose work-in-progress.

- [`git co`](./git-co.md) ✅ — Shortcut for `git checkout`. Parameters are forwarded.

- [`git sw`](./git-sw.md) ✅ — Alias for `git switch`. Parameters are forwarded.

- [`git delete`](./git-delete.md) — Delete a local branch, but only if it's changes have been merged elsewhere.

- [`git fell`](./git-fell.md) — Delete any branches that have already been merged into the default branch or the specified branch.

- [`git branches`](./git-branches.md) — List all branches by order of last commit.

- [`git tracking`](./git-tracking.md) — Same as `git branches` but also shows the names of the tracked upstream branches.

- [`git current`](./git-current.md) — Show the name of the current branch.

- [`git default`](./git-default.md) — Show the name of the default branch, as configured in the "origin" repo.

- [`git backup`](./git-backup.md) — Create a backup of the current branch or another specified branch.

## Tagging

- [`git tags`](./git-tags.md) — List all tags, sorted by commit date.

- [`git versions`](./git-versions.md) — List tags prefixed with the lower case letter "v", sorted numerically.

## Staging

- [`git state`](./git-state.md) — Concise view of `git status`.

- [`git working`](./git-working.md) — List all changed files in the working directory.

- [`git staged`](./git-staged.md) — List files with changes staged for committing.

- [`git track`](./git-track.md) — Start tracking a new file. This is an alias for `git add` and the opposite of the `git untrack` alias.

- [`git untrack`](./git-untrack.md) — Untrack a specified file.

## Ignoring

- [`git ignored`](./git-ignored.md) — List all ignored files.

- [`git ignore`](./git-ignore.md) — Ignore changes made to the specified file.

- [`git unignore`](./git-unignore.md) — Stop ignoring changes made to a file.

## Committing

- [`git cm`](./git-cm.md) — Shortcut for `git add . && git commit`. Stage and commit all changes in the working directory, including new (untracked) files. If a message is provided, it is used as the commit message; otherwise, the user will be prompted to input a message.

- [`git wip`](./git-wip.md) — Save work-in-progress. Creates a commit, with the contents of the staging index plus working directory, with the specified message (or "WIP" if no message is provided). Continue where you left off tomorrow with `git resume`.

- [`git resume`](./git-resume.md) — Resume work-in-progress committed via the last `git wip` operation.

## Redoing commits

- [`git amend`](./git-amend.md) ✅ — Add all working changes to last commit, including new (untracked) files.

- [`git unamend`](./git-unamend.md) ✅ — Undo the prior `git amend` or `git commit --amend` operation.

- [`git reword`](./git-reword.md) — Change the message of the most recent commit or an earlier specified commit. Anything staged will get added to the newly recreated commit, too.

- [`git fixup`](./git-fixup.md) — Fix something in the most recent commit or an earlier specified commit. Rewrites history.

## Undoing changes

- [`git uncommit`](./git-uncommit.md) ✅ — Undo the last commit, returning the changes introduced in the commit to the staging index.

- [`git discard`](./git-discard.md) — Discard working changes to one or more files. Changes made will be lost indefinitely.

- [`git unstage`](./git-unstage.md) — Alias for `git reset --mixed HEAD`, which just removes everything from the staging index, returning those changes to the working directory.

- [`git undo`](./git-undo.md) — Reset to the last commit, undoing all staged and working changes. A save-point commit is made, so the work will be recoverable using `git reflog`.

<!-- TODO: `git rewind` to change the HEAD of the current branch to an earlier commit. -->

## Merging

- [`git ff`](./git-ff.md) — Perform a fast-forward merge.

- [`git squash`](./git-squash.md) — Perform a `git merge --squash` operation.

- [`git pick`](./git-pick.md) — Shortcut for `git cherry-pick`. Parameters are forwarded.

## Pushing and pulling

- [`git down`](./git-down.md) — Shortcut for `git pull` with the rebase merge strategy (ie. `git pull --rebase`).

- [`git up`](./git-up.md) — Push new commits up to the tracked upstream branch (else to a new branch of the same name, if tracking is not yet established). Pushes tags and sets up tracking, too. Add the `--force` option to remove commits from the upstream branch that do not exist in the local branch – unless those commits were introduced by someone else.

- [`git sync`](./git-sync.md) — Sync the local checked-out branch with its tracked upstream branch, maintaining linear history.

- [`git push-all`](./git-push-all.md) — Push changes in all local branches to their tracked branches in the remote repository. Defaults to the "origin" remote unless otherwise specified.

- [`git rebase-all`](./git-rebase-all.md) — Rebase all local branches on the trunk branch. Defaults to using the `main` branch as the target base branch, unless otherwise specified.

- [`git upstream`](./git-upstream.md) — Show the name of the tracked upstream repository.

- [`git remotes`](./git-remotes.md) — List the URLs of all remotes.

- [`git download`](./git-download.md) — Improved `git fetch`: download and prune local objects, tags, and branches to match all remotes.

## Stashing

- [`git stashed`](./git-stashed.md) — Show the current number of stash entries.

<!-- TODO: More stash aliases. -->

## Logs

- [`git history`](./git-history.md) — Clean `git log`, paginated.

- [`git recent`](./git-recent.md) — Clean `git log`, last 25 entries only.

- [`git graph`](./git-graph.md) — Show a detailed graphical representation of the commit history; alternative to `git log`.

- [`git last`](./git-last.md) — Show detailed information on the changes in the last commit.

- [`git filelog`](./git-filelog.md) — List all the commits that have changed the specified file.

- [`git changes`](./git-changes.md) — Show the changes introduced in a specified commit, or introduced to the working directory plus staging index since the last commit.

- [`git fetched`](./git-fetched.md) — List the commits added by the last `git fetch` operation.

- [`git author`](./git-author.md) ✅ — Change the author of the last commit or an earlier specified commit.

- [`git contrib`](./git-contrib.md) ✅ — List all contributors, ordered by their total commit count.

## Configuration

- [`git configure`](./git-configure.md) — Open `~/.gitconfig` in your default text editor.

- [`git whoami`](./git-whoami.md) ✅ — Show information about the configured Git user.
