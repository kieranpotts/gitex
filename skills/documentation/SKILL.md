---
name: documentation
description: Formatting conventions for the AsciiDoc docs in docs/, including per-command usage files.
compatibility: requires asciidoc-compatible tooling (optional, for preview)
license: MIT
---

# Documentation

Use this skill when authoring or modifying any `.adoc` file in `docs/` (or the top-level [`README.adoc`](../../README.adoc)). General language rules - American English, full sentences, periods - live in [`../../AGENTS.md`](../../AGENTS.md) and apply here too.

Do NOT use this skill for in-code comments (those follow the shell-scripts or python-tests skill) or for the project's Markdown files.

## Instructions

1. **Place the file correctly.**
   - `docs/requirements.adoc`: supported platforms.
   - `docs/installation.adoc`: install instructions for end users.
   - `docs/configuration.adoc`: environment variables and their effects.
   - `docs/runtime-tests.adoc`: how to run the pytest suite.
   - `docs/static-analysis.adoc`: how to run ShellCheck and Ruff.
   - `docs/usage/README.adoc`: hand-maintained index of all per-command usage docs.
   - `docs/usage/git-<name>.adoc`: one usage doc per Git extension.

   When adding or renaming a script in `bin/`, both the per-command file and the indexes in `docs/usage/README.adoc` and the top-level [`README.adoc`](../../README.adoc) must be updated together. See [`../new-command/SKILL.md`](../new-command/SKILL.md).

2. **Follow the canonical usage-doc shape** ([`docs/usage/git-whoami.adoc`](../../docs/usage/git-whoami.adoc)):

   ```adoc
   = `git <name>`

   <One-line summary in prose.>

   <One or two paragraphs explaining behavior, edge cases, mechanics.>

   == Usage

   ----
   $ git <name> [args]
   ----

   <Brief notes on arguments, or "This command does not accept any arguments.">

   == Examples

   <Realistic command + output blocks, with prose framing.>

   == See also

   * link:./git-other.adoc[`git other`]: <one-line cross-reference>.
   ```

   For destructive commands, add a `CAUTION:` admonition near the top, as in [`docs/usage/git-amend.adoc`](../../docs/usage/git-amend.adoc).

3. **Use the project's AsciiDoc conventions.**
   - **Headings.** `=` for the document title (one per file; always `` `git <name>` `` for usage docs), `==` for sections, `===` for sub-sections.
   - **Listing blocks** (command output, untyped code):

     ```adoc
     ----
     $ git whoami
     name:  Kieran Potts
     ----
     ```

   - **Source blocks** (code with a language, for highlighting):

     ```adoc
     [source,bash]
     ----
     if [ -d "$HOME/dev/gitex/bin" ] ; then
       PATH="$PATH:$HOME/dev/gitex/bin"
     fi
     ----
     ```

   - **Internal links.** `link:./path/file.adoc[Display Text]`.

4. **Wrap lines around 72 columns.** The project's VS Code workspace settings enforce this for AsciiDoc to keep diffs readable.

## Examples

Inline admonition (single paragraph):

```adoc
CAUTION: This command rewrites commit history.
```

Block admonition (multiple paragraphs, lists, or formatting):

```adoc
[WARNING]
======
Longer warning text that needs multiple
paragraphs.

Continues here.
======
```

Valid labels: `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`.

## Edge cases

- The cross-link list in [`docs/usage/git-amend.adoc`](../../docs/usage/git-amend.adoc) floats below the body without a `== See also` heading. This is inconsistent with `git-whoami.adoc`; treat `git-whoami.adoc` as the canonical layout.
- The hand-maintained command index appears in two places ([`README.adoc`](../../README.adoc) and [`docs/usage/README.adoc`](../../docs/usage/README.adoc)). Both must be updated together.
- Stub usage docs often exist before the matching `bin/` script is implemented — they encode the intended CLI design. When implementing, verify rather than rewrite.

## References

- [`docs/usage/git-whoami.adoc`](../../docs/usage/git-whoami.adoc): canonical usage-doc template.
- [`docs/usage/git-amend.adoc`](../../docs/usage/git-amend.adoc): example with a `CAUTION:` admonition.
- [`../../AGENTS.md`](../../AGENTS.md): global language rules.
- [`../new-command/SKILL.md`](../new-command/SKILL.md): adding a new command and its docs together.
