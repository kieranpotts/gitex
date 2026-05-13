# Documentation (`docs/`)

User and developer documentation is written in AsciiDoc (`.adoc`).

## Layout

- `docs/requirements.adoc`, `docs/installation.adoc` — setup instructions.
- `docs/usage/<command>.adoc` — one file per Git extension. When adding or renaming a script in `bin/`, update the corresponding usage doc.
- `docs/runtime-tests.adoc`, `docs/static-analysis.adoc` — development process docs.

## Conventions

- Internal links use the AsciiDoc form: `link:./path/file.adoc[Display Text]`.
- Use American English and full sentences (terminated with periods), consistent with code comments.
