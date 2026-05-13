# Commit messages

Commit message format is enforced by CI via the `kieranpotts/actions/validate-commits` action, wired up in [`.github/workflows/commit-validation.yaml`](../../.github/workflows/commit-validation.yaml). Commits that fail validation block PRs.

## Format

```
<type>: <subject>
```

Validation regex (only the subject line is checked):

```
^((chore|dev|feature|fix|maintenance|merge|performance|refactor|release|revert): [a-z].*)$
```

Rules:

- `<type>` must be one of the ten literal strings above.
- `<subject>` must begin with a lowercase letter.
- No period at the end of the subject.
- Bodies are unconstrained but conventionally omitted in this project.
- Scopes/parentheticals (`feature(parser): …`) fail validation — the regex expects the colon immediately after the type.

## Type semantics

Derived from how the types are actually used in the project's history:

- `feature` — new user-facing capability (new command, new flag, new env var).
- `fix` — bug fix in an existing capability.
- `performance` — performance improvement, no behavioural change.
- `refactor` — internal restructuring with no behavioural change (renames, helper extraction, simplifying interfaces).
- `dev` — development-time artifacts that don't ship to users: tests, roadmap, dev scripts, project-internal tooling.
- `maintenance` — repo/workspace hygiene: VS Code config, devcontainer, CI workflows, label sync, dependency bumps.
- `chore` — minor uncategorised work: typo fixes, comment tweaks, formatting.
- `release` — version bumps and release tags.
- `merge` — merge commits (when not fast-forwarded away).
- `revert` — reverting a prior commit.

The `dev` / `maintenance` / `chore` boundary is fuzzy. Rule of thumb: `dev` touches the dev loop (tests, roadmap); `maintenance` touches infrastructure (CI, container, workspace); `chore` is everything else small.

## Examples

From recent history:

```
feature: add git uncommit
fix: handle empty repository in git-amend
refactor: simplify test repo interface
dev: add implementation roadmap
maintenance: reinstate markdown handling in vs code
chore: small docs fix
```

## Local validation

There is no local hook — the validator only runs in CI. To check messages on the current branch before pushing:

```sh
git log --format=%s origin/dev..HEAD | \
  grep -Ev '^(chore|dev|feature|fix|maintenance|merge|performance|refactor|release|revert): [a-z]'
```

Empty output means all commits will pass. (Substitute `origin/main` if the trunk has moved.)

## Not validated, but conventional

- Imperative present-tense: "add X", not "added X" or "adds X".
- Subject ≤ ~72 characters, so `git log --oneline` stays readable.
- One logical change per commit. Refactors are usually split into many small commits in this project; feature work tends to bundle.
