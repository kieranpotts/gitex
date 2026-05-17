---
name: documentation
description: Formatting conventions for the Markdown docs.
compatibility: none required
license: MIT
---

# Documentation

Use this skill when authoring or modifying any `.md` file in `docs/` or the top-level `README.md`.

Do NOT use this skill for in-code comments (those follow the shell-scripts or python-tests skills).

## Rules

-   **American English.**

-   **Full sentences terminated by periods.**

-   **Place documentation in the right place:**

    - `docs/requirements.md`: Supported platforms.
    - `docs/installation.md`: Install instructions for end users.
    - `docs/configuration.md`: Environment variables and their effects.
    - `docs/static-analysis.md`: How to run ShellCheck and Ruff.
    - `docs/runtime-tests.md`: How to run the pytest suite.
    - `docs/usage/README.md`: Hand-maintained index of all per-command usage docs.
    - `docs/usage/git-<name>.md`: One usage doc per Git extension.

-   **Maintain consistency.**

    When changing scripts in `bin`, make sure the following files are updated simultaneously, as necessary:

    - The command's documentation: `docs/usage/<command>.md`.
    - The command index: `docs/usage/README.md`.
    - The top-level `README.md` file.
    - The top-level `TODO.md` file.
    - The `_print_commands()` function in the [`bin/gitex`](../../bin/gitex) script, which outputs a list of subcommands.

-   **Follow this template for usage docs:**

    ````
    # `git <name>`

    One-line summary in prose.

    One or two paragraphs explaining behavior, edge cases, mechanics.

    > [!CAUTION]
    > Warn users if this is a particularly destructive command, for example if it rewrites history.

    ## Usage

    ```
    $ git <name> [args]
    ```

    Brief notes on arguments, or "This command does not accept any arguments."

    ## Examples

    Realistic command + output blocks, with prose framing.

    ## See also

    - [`git other`](./git-other.md): One-line description.
    ````

-   **Follow the project's Markdown conventions,** including but not limited to:

    - **Headings**: `#` for the document title (one per file; always `` `git <name>` `` for usage docs), `##` for sections, `###` for sub-sections.

    - **Bullets**: `-` (not `*` or `+`). Nested bullets indent by two spaces.

    - **Emphasis**: `**bold**`, `*italic*` (use sparingly).

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

    - **Internal links:** `[Display Text](./path/file.md)`. Relative paths from the file's own location.

-   **Do not hard-wrap lines:**

    Line length MUST NOT be enforced in Markdown files directly. The project's VS Code workspace settings implement a visual wrap at 72 for `.md` files, for readability.

-   **Use a subset of GitHub-Flavored Markdown.**

    See https://github.github.com/gfm/.

-   **GitHub-flavored callouts are allowed.**

    They render as styled admonition boxes on GitHub, and elsewhere they degrade to a plain blockquote with `[!LABEL]` shown as literal text.

-   **Stubbed usage docs may be used for API design.**

    Stubbed usage docs may therefore be out-of-sync with the implementation. Verify the implementation before modifying documentation.

## Examples

GitHub-flavored callout:

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
