# GitEx Implementation Roadmap

This checklist tracks the implementation status of the GitEx commands as defined in the usage documentation.

## Status

Last reviewed on 2026-10-26.

A command is ticked only when it has all of:

- a working implementation in `bin/`;
- a real test suite in `test/`;
- and a usage doc in `docs/usage/`.

Every unticked command is scaffolded but not implemented. Each one has:

- A script in `bin/` with a header comment and a rough draft body, marked `# TODO: Review draft implementation`. The drafts have not been reviewed and some do not run. Some also contain Bashisms that must be removed.

- A placeholder test file in `test/`, with the test body commented out.

- A usage doc in `docs/usage/`, which may describe intended rather than actual behavior.

Use [`.agents/skills/new-command/SKILL.md`](.agents/skills/new-command/SKILL.md) as the checklist when finishing each command.

## GitEx
- [x] `gitex`

## Cloning
- [x] `git cl`

## Branching
- [x] `git br`
- [x] `git orphan`
- [x] `git co`
- [x] `git sw`
- [ ] `git delete` (The draft rejects any argument before reading the branch name, and uses Bash array syntax.)
- [ ] `git fell`
- [ ] `git branches`
- [ ] `git tracking`
- [ ] `git current`
- [ ] `git default`
- [ ] `git backup`

## Tagging
- [ ] `git tags`
- [ ] `git versions`

## Staging
- [ ] `git state`
- [ ] `git working`
- [ ] `git staged`
- [ ] `git track`
- [ ] `git untrack`

## Ignoring
- [ ] `git ignored`
- [ ] `git ignore`
- [ ] `git unignore`

## Committing
- [ ] `git cm`
- [ ] `git wip`
- [ ] `git resume`

## Redoing commits
- [x] `git amend`
- [x] `git unamend`
- [ ] `git reword`
- [ ] `git fixup`

## Undoing changes
- [x] `git uncommit`
- [ ] `git discard`
- [ ] `git unstage`
- [ ] `git undo`
- [ ] `git rewind` (Planned)

## Merging
- [ ] `git ff`
- [ ] `git squash`
- [ ] `git pick`

## Pushing and pulling
- [ ] `git down`
- [ ] `git up`
- [ ] `git sync`
- [ ] `git push-all`
- [ ] `git rebase-all`
- [ ] `git upstream`
- [ ] `git remotes`
- [ ] `git download`

## Stashing
- [ ] `git stashed`
- [ ] Other stash aliases (Planned)

## Logs
- [ ] `git history`
- [ ] `git recent`
- [ ] `git graph`
- [ ] `git last`
- [ ] `git filelog`
- [ ] `git changes`
- [ ] `git fetched`
- [x] `git author`
- [x] `git contrib`

## Configuration
- [ ] `git configure`
- [x] `git whoami`

## Dev tooling

### Scratch repository for manual testing

Proposal for a throwaway repository in which to try the GitEx commands by hand, alongside the automated tests.

- [ ] Add `run/scratch` and a matching `make scratch` target, following the existing `run/` and `Makefile` pattern.

- [ ] Build the scratch environment in a gitignored `.scratch/` directory inside the worktree, so it works identically on the host and in the devcontainer and its files can be opened in the editor. Add `/.scratch/` to `.gitignore`.

- [ ] Guard against operating on the GitEx repository itself. A nested repository whose `.git` is missing lets Git discover the parent repository, so a destructive command such as `git uncommit` would rewrite GitEx's own history. The launcher must set `GIT_CEILING_DIRECTORIES` to the scratch directory's parent, and refuse to start unless `.scratch/repo/.git` exists.

- [ ] Rebuild from scratch on every run, so that state consumed by destructive commands (amend, squash, undo) can be restored with one command.

- [ ] Seed the fixtures that the commands need:
  - a few commits on `main`, a feature branch, and a tag;
  - a bare `.scratch/origin.git` remote, for `sync`, `up`, `down`, `push-all`, `upstream`, and `fetched`;
  - optionally, a second clone acting as a teammate, to produce a diverged upstream;
  - staged and unstaged changes, for `state`, `staged`, `working`, and `discard`.

- [ ] Write the seeding in shell rather than reusing `test/helper.py`, so the launcher does not depend on Poetry.

- [ ] Isolate the developer's own Git configuration by pointing `GIT_CONFIG_GLOBAL` at a scratch config with a dummy identity and commit signing disabled. Offer a `--real-config` flag to opt back in.

- [ ] Open a subshell in `.scratch/repo` with `bin/` prepended to `PATH`. Exiting the subshell returns to the caller's directory.

- [ ] Support `--shell <sh|bash|zsh>`. The interactive shell does not determine which shell runs the scripts, because each script's shebang does. So the launcher must generate a shim directory, prepended to `PATH`, in which each `git-<name>` runs `exec <shell> /abs/path/bin/git-<name> "$@"`.

- [ ] Apply the same approach to the pytest suite, parametrizing the `bin` fixture over `sh`, `bash`, and `zsh`.
