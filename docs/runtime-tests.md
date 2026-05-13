# Runtime tests

Execution of the runtime tests requires the following dependencies to be installed on your machine:

- Python >= 3.12
- Poetry >= 2.2

To avoid needing to add this software to your machine, you can instead open this project in a [dev container](https://containers.dev/). In VS Code, open this repository in its own workspace, then select "Dev Containers: Reopen in Dev Container" from the command palette. This will reopen the project in a Docker container, in which all of the development dependencies will be already installed. This has the added benefit of creating an isolated environment in which you can safely run the automated tests, and manually test the Git aliases, without risk of contaminating your own local Git configuration.

[Poetry](https://github.com/python-poetry/poetry) is used to manage the Python development dependencies for the GitEx project. Run the below command in the root directory of this repository to install pytest and other dependencies in a virtual environment. (This command will have already been run when you launch the dev container.)

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
> $ ./check
> ```
>
> In the dev container, you will need to use the following command instead:
>
> ```
> $ bash check
> ```
>
> Remember to give yourself executable privileges on this file:
>
> ```
> $ chmod u+x check
> ```
