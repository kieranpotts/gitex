# Runtime tests

Execution of the runtime tests requires [mise](https://mise.jdx.dev) to be installed on your machine. mise installs the versions of Python, Poetry, and ShellCheck that are pinned in [`mise.toml`](../mise.toml), so that the same versions are used on every machine and in the dev container. To set up the project, run:

```
$ ./run/install
```

This trusts the project's `mise.toml` (`mise trust`), installs the pinned toolchain (`mise install`), and then installs the Python test dependencies (`poetry install`).

This project does not ship a [dev container](https://containers.dev/) of its own. If you work in one anyway, for example to manually test the Git aliases without risk of contaminating your own Git configuration, make sure it has mise installed, then run `./run/install` inside it.

[Poetry](https://github.com/python-poetry/poetry) is used to manage the Python development dependencies for the GitEx project. Run the below command in the root directory of this repository to install pytest and other dependencies in a virtual environment. (`./run/install` runs it for you.)

```
$ poetry install
```

The tests are run by [pytest](https://github.com/pytest-dev/pytest/). To execute the tests, run the following command from the root directory of this repository:

```
$ poetry run pytest
```

Or, for more verbose output:

```
$ poetry run pytest -v
```

Tests can be run individually:

```
$ poetry run pytest test/test_git_backup.py
```

The tests use [Git Python](https://github.com/gitpython-developers/GitPython) to dynamically create temporary Git repositories, and the tests do not change any global or user-level Git configuration (only local), ensuring isolation and no interference with your own Git configuration.

> [!TIP]
> All runtime tests can be executed with this shortcut:
>
> ```
> $ ./run/check
> ```
