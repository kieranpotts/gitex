---
name: commits
description: Commit-message format enforced by CI, and the semantics of each allowed type.
compatibility: requires git
license: MIT
---

# Commits

Use this skill when composing a commit message, validating a branch's messages before push, or troubleshooting a failed `commit-validation` CI job.

The format is enforced by the `kieranpotts/actions/validate-commits` action, wired up in [`.github/workflows/commit-validation.yaml`](../../.github/workflows/commit-validation.yaml). Failing commits block PRs.

Do NOT use this skill for branch-naming conventions or PR titles - neither is currently enforced.

## Instructions

1. **Use the exact format:**

   ```
   <type>: <subject>
   ```

   Validation regex (only the subject line is checked):

   ```
   ^((chore|dev|feature|fix|maintenance|merge|performance|refactor|release|revert): [a-z].*)$
   ```

2. **Follow the rules:**
   - `<type>` must be one of the ten literal strings above.
   - `<subject>` must begin with a lowercase letter.
   - No period at the end of the subject.
   - Bodies are unconstrained but conventionally omitted.
   - Scopes/parentheticals (`feature(parser): …`) fail validation - the regex expects the colon immediately after the type.

3. **Pick the type by semantic, not by file extension:**
   - `feature`: new user-facing capability (new command, new flag, new env var).
   - `fix`: bug fix in an existing capability.
   - `performance`: performance improvement, no behavioral change.
   - `refactor`: internal restructuring with no behavioral change (renames, helper extraction, simplifying interfaces).
   - `dev`: development-time artifacts that don't ship to users - tests, roadmap, dev scripts, project-internal tooling.
   - `maintenance`: repo/workspace hygiene - VS Code config, devcontainer, CI workflows, label sync, dependency bumps.
   - `chore`: minor uncategorized work - typo fixes, comment tweaks, formatting.
   - `release`: version bumps and release tags.
   - `merge`: merge commits (when not fast-forwarded away).
   - `revert`: reverting a prior commit.

   The `dev` / `maintenance` / `chore` boundary is fuzzy. Rule of thumb: `dev` touches the dev loop (tests, roadmap); `maintenance` touches infrastructure (CI, container, workspace); `chore` is everything else small.

4. **Validate locally before pushing** (there is no pre-commit hook):

   ```sh
   git log --format=%s origin/dev..HEAD | \
     grep -Ev '^(chore|dev|feature|fix|maintenance|merge|performance|refactor|release|revert): [a-z]'
   ```

   Empty output means all commits will pass. Substitute `origin/main` if the trunk has moved.

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

## Edge cases

- **Conventional but not validated:** imperative present-tense ("add X", not "added"/"adds"), subject ≤ ~72 characters for `git log --oneline` readability, one logical change per commit. Refactors are typically split into many small commits in this project; feature work tends to bundle.
- **Capital letter at the start of the subject fails validation** even though English style would capitalize. Stay lowercase.
- **`feature(scope): …` fails.** Scopes are not supported by the regex.

## References

- [`.github/workflows/commit-validation.yaml`](../../.github/workflows/commit-validation.yaml): workflow that runs the validator.
- [`../testing/SKILL.md`](../testing/SKILL.md): `./check` does NOT run commit validation; CI does.
- [`../new-command/SKILL.md`](../new-command/SKILL.md): new commands ship as `feature: …`.
