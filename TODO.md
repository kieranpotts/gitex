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

Use [`skills/new-command/SKILL.md`](skills/new-command/SKILL.md) as the checklist when finishing each command.

## GitEx
- [x] `gitex`

## Cloning
- [x] `git cl`

## Branching
- [x] `git br`
- [ ] `git orphan` (In progress; see *Work in progress*.)
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
