# User documentation

- Prose MUST be in American English, written as full sentences terminated by
  periods.

- A usage doc for a destructive command — one that rewrites history, deletes
  refs, or discards work — MUST carry a `[!CAUTION]` callout directly after the
  introductory paragraphs. Other commands MUST NOT carry one.

- Prose SHOULD be hard-wrapped at 80 characters. Tables and long URLs MAY run
  longer. A line MUST NOT break inside a link, code span, or emphasis — because
  a break there can silently fail to render the inline formatting.

- Code blocks MUST be fenced. Command lines and their output SHOULD use a bare
  fence, with each command prefixed by `$ `. Source code, rather than commands,
  SHOULD use a fence tagged with its language, eg. `sh` or `bash`.

- Markdown SHOULD stay within CommonMark plus three GitHub extensions: tables,
  task lists, and alerts. Other extensions degrade badly outside GitHub.

- Alerts MUST use one of the labels `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, or
  `CAUTION`. Outside GitHub they render as a plain blockquote, so the text MUST
  still read sensibly with the `[!LABEL]` marker shown literally. Example:

  ```markdown
  > [!CAUTION]
  > This command rewrites commit history.
  ```

- There MUST be exactly one level 1 heading per Markdown file.

- Markdown files must use ATX-style headings. Nested headings MUST step down
  exactly one level at a time.

- The hyphen character (`-`) MUST be used for bullets.

- Emphasis SHOULD be used sparingly.

- Links MUST be relative to the file's own location.

- Every relative link MUST resolve to an existing file in the same repository.
