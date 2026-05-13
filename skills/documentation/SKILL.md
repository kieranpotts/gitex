# Documentation (`docs/`)

User and developer documentation is written in AsciiDoc (`.adoc`). General language rules (American English, full sentences, periods) are in [`../../AGENTS.md`](../../AGENTS.md) and apply here too.

## Layout

- `docs/requirements.adoc` — Supported platforms.
- `docs/installation.adoc` — Install instructions for end users.
- `docs/configuration.adoc` — Environment variables and their effects.
- `docs/runtime-tests.adoc` — How to run the pytest suite.
- `docs/static-analysis.adoc` — How to run ShellCheck and Ruff.
- `docs/usage/README.adoc` — Hand-maintained index of all per-command usage docs.
- `docs/usage/git-<name>.adoc` — One usage doc per Git extension. Use [`docs/usage/git-whoami.adoc`](../../docs/usage/git-whoami.adoc) as the canonical template.

When adding or renaming a script in `bin/`, both `docs/usage/git-<name>.adoc` and the index in `docs/usage/README.adoc` (and the top-level [`README.adoc`](../../README.adoc)) must be updated. See [`../new-command/SKILL.md`](../new-command/SKILL.md).

## Usage doc structure

Follow the shape of [`docs/usage/git-whoami.adoc`](../../docs/usage/git-whoami.adoc):

```adoc
= `git <name>`

<One-line summary in prose.>

<One or two paragraphs explaining behaviour, edge cases, and any non-obvious mechanics.>

== Usage

----
$ git <name> [args]
----

<Brief notes on arguments, or "This command does not accept any arguments.">

== Examples

<Realistic command + output blocks, with prose framing.>

== See also

* link:./git-other.adoc[`git other`] — <one-line cross-reference>.
```

For commands that rewrite history or perform other destructive operations, add a `CAUTION:` admonition near the top, as in [`docs/usage/git-amend.adoc`](../../docs/usage/git-amend.adoc).

## AsciiDoc conventions

**Headings.** `=` for the document title (one per file), `==` for sections, `===` for sub-sections. Title is the literal `git <name>` in backticks.

**Listing blocks** (command output, code with no language):

```adoc
----
$ git whoami
name:  Kieran Potts
----
```

**Source blocks** (code with a language, for syntax highlighting):

```adoc
[source,bash]
----
if [ -d "$HOME/dev/gitex/bin" ] ; then
  PATH="$PATH:$HOME/dev/gitex/bin"
fi
----
```

**Admonitions.** Two forms; pick by length:

- *Inline* (single paragraph): `CAUTION: This command rewrites commit history.`
- *Block* (multiple paragraphs / lists):

  ```adoc
  [WARNING]
  ======
  Longer warning text that needs
  multiple paragraphs or formatting.
  ======
  ```

  Valid labels: `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`.

**Internal links.** Use the AsciiDoc form: `link:./path/file.adoc[Display Text]`. Cross-references between usage docs go in the `== See also` section.

**Line wrapping.** The project's VS Code settings wrap AsciiDoc at 72 columns; keep lines around that length where practical for readable diffs.
