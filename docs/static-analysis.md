# Static analysis

[ShellCheck](https://github.com/koalaman/shellcheck) is used for static analysis of the shell scripts. Its version is pinned in [`mise.toml`](../mise.toml), because different ShellCheck versions report different findings. `./run/install` installs it, along with the rest of the toolchain — see [Runtime tests](./runtime-tests.md).

To run the linter on all the shell scripts in the `bin` directory, run the following command from the root directory of this repository:

```
$ shellcheck --severity=style bin/* lib/*
```

(Other ShellCheck severity levels, in declining order of severity, are: "error", "warning", "info", and "style" (https://github.com/koalaman/shellcheck/blob/eac8efff9c41bf90416b53a72209903aa9213bdb/shellcheck.1.md?plain=1#L106[reference).)

[Ruff](https://github.com/astral-sh/ruff) is used to lint and format the Python code used in the runtime tests. Installation of Ruff is managed by Poetry – see [Runtime tests](./runtime-tests.md) for details.

To run Ruff, use the following commands from the root directory of this repository:

```
$ poetry run ruff check test/
$ poetry run ruff format test/
```

The formatter should be run before committing any changes to the Python test files.

> [!TIP]
> Automated formatting can be applied using this shortcut:
>
> ```
> $ ./run/fix
> ```
