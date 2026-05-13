---
name: documentation
description: Formatting conventions for the Markdown docs in docs/, including per-command usage files.
compatibility: none required
license: MIT
metadata:
  project: gitex
---

# Documentation

Use this skill when authoring or modifying any `.md` file in `docs/` (or the top-level [`README.md`](../../README.md)). General language rules - American English, full sentences, periods - live in [`../../AGENTS.md`](../../AGENTS.md) and apply here too.

Do NOT use this skill for in-code comments (those follow the shell-scripts or python-tests skill) or for the `TODO.md` checklist.

## Instructions

1. **Place the file correctly.**
   - `docs/requirements.md`: supported platforms.
   - `docs/installation.md`: install instructions for end users.
   - `docs/configuration.md`: environment variables and their effects.
   - `docs/runtime-tests.md`: how to run the pytest suite.
   - `docs/static-analysis.md`: how to run ShellCheck and Ruff.
   - `docs/usage/README.md`: hand-maintained index of all per-command usage docs.
   - `docs/usage/git-<name>.md`: one usage doc per Git extension.

   When adding or renaming a script in `bin/`, both the per-command file and the indexes in `docs/usage/README.md` and the top-level [`README.md`](../../README.md) must be updated together. See [`../new-command/SKILL.md`](../new-command/SKILL.md).

2. **Follow the canonical usage-doc shape** ([`docs/usage/git-whoami.md`](../../docs/usage/git-whoami.md)):

   ````
   # `git <name>`

   <One-line summary in prose.>

   <One or two paragraphs explaining behavior, edge cases, mechanics.>

   ## Usage

   ```
   $ git <name> [args]
   ```

   <Brief notes on arguments, or "This command does not accept any arguments.">

   ## Examples

   <Realistic command + output blocks, with prose framing.>

   ## See also

   - [`git other`](./git-other.md): <one-line cross-reference>.
   ````

   For destructive commands, add a `> [!CAUTION]` admonition near the top, as in [`docs/usage/git-amend.md`](../../docs/usage/git-amend.md).

3. **Use the project's Markdown conventions.**
   - **Headings.** `#` for the document title (one per file; always `` `git <name>` `` for usage docs), `##` for sections, `###` for sub-sections.
   - **Bullets.** `-` (not `*` or `+`). Nested bullets indent by two spaces.
   - **Emphasis.** `**bold**`, `*italic*` (use sparingly).
   - **Fenced code blocks** for command output and untyped code:

     ````
     ```
     $ git whoami
     name:  Kieran Potts
     ```
     ````

   - **Language-tagged fences** for syntax-highlighted code:

     ````
     ```bash
     if [ -d "$HOME/dev/gitex/bin" ] ; then
       PATH="$PATH:$HOME/dev/gitex/bin"
     fi
     ```
     ````

   - **Internal links.** `[Display Text](./path/file.md)`. Relative paths from the file's own location.

4. **Wrap lines around 72 columns.** The project's VS Code workspace settings enforce a visual wrap at 72 for `.md` files to keep diffs readable. Long URLs and code lines may exceed; prose should not.

## Examples

GitHub callout admonitions (render as styled boxes on GitHub, degrade to plain blockquotes elsewhere):

```
> [!CAUTION]
> This command rewrites commit history.
```

Block form with multiple paragraphs or nested code:

````
> [!TIP]
> All runtime tests can be executed with this shortcut:
>
> ```
> $ ./check
> ```
````

Valid labels: `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`.

## Edge cases

- **GitHub callouts are renderer-specific.** They render as styled admonition boxes on GitHub and a few other renderers. Elsewhere they degrade to a plain blockquote with `[!LABEL]` shown as literal text. Acceptable trade-off; this project is primarily browsed on GitHub.
- **Nested code fences inside admonitions** must keep the `> ` blockquote prefix on every line, including the inner triple-backticks. See [`docs/runtime-tests.md`](../../docs/runtime-tests.md) for a working example.
- **The cross-link list in [`docs/usage/git-amend.md`](../../docs/usage/git-amend.md)** floats below the body without a `## See also` heading. This is inconsistent with `git-whoami.md`; treat `git-whoami.md` as the canonical layout.
- **The hand-maintained command index appears in two places** ([`README.md`](../../README.md) and [`docs/usage/README.md`](../../docs/usage/README.md)). Both must be updated together.
- **Stub usage docs often exist before the matching `bin/` script is implemented** - they encode the intended CLI design. When implementing, verify rather than rewrite.

## References

- [`docs/usage/git-whoami.md`](../../docs/usage/git-whoami.md): canonical usage-doc template.
- [`docs/usage/git-amend.md`](../../docs/usage/git-amend.md): example with a `> [!CAUTION]` admonition.
- [`docs/runtime-tests.md`](../../docs/runtime-tests.md): example with a `> [!TIP]` block containing nested code fences.
- [`../../AGENTS.md`](../../AGENTS.md): global language rules.
- [`../new-command/SKILL.md`](../new-command/SKILL.md): adding a new command and its docs together.
