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
- Scopes/parentheticals (`feature(parser): …`) fail validation. The regex expects the colon immediately after the type.

## Type semantics

Derived from how the types are actually used in the project's history:

- `feature`: New user-facing capability (new command, new flag, new env var).
- `fix`: Bug fix in an existing capability.
- `performance`: Performance improvement, no behavioral change.
- `refactor`: Internal restructuring with no behavioral change (renames, helper extraction, simplifying interfaces).
- `dev`: Development-time artifacts that don't ship to users: tests, roadmap, dev scripts, project-internal tooling.
- `maintenance`: Repo/workspace hygiene: VS Code config, devcontainer, CI workflows, label sync, dependency bumps.
- `chore`: Minor uncategorised work: typo fixes, comment tweaks, formatting.
- `release`: Version bumps and release tags.
- `merge`: Merge commits (when not fast-forwarded away).
- `revert`: Reverting a prior commit.

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

There is no local hook. The validator only runs in CI. To check messages on the current branch before pushing:

```sh
git log --format=%s origin/dev..HEAD | \
  grep -Ev '^(chore|dev|feature|fix|maintenance|merge|performance|refactor|release|revert): [a-z]'
```

Empty output means all commits will pass. (Substitute `origin/main` if the trunk has moved.)

## Not validated, but conventional

- Imperative present-tense: "add X", not "added X" or "adds X".
- Subject ≤ ~72 characters, so `git log --oneline` stays readable.
- One logical change per commit. Refactors are usually split into many small commits in this project; feature work tends to bundle.
