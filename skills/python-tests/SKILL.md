# Python tests (`test/`)

Tests use pytest with GitPython to create isolated temporary repositories.

## Layout

- `conftest.py`: pytest configuration with fixtures such as `repo`.
- `helper.py`: `TestRepo` class for creating isolated temporary Git repositories using GitPython.
- `test_<command>.py`: One test file per Git extension (e.g. `test_git_whoami.py` tests `git whoami`).

See `test/test_git_whoami.py` for a canonical example.

## Running tests

```bash
poetry install                              # Install dependencies.
poetry run pytest                           # Run the full suite.
poetry run pytest -v                        # Verbose output.
poetry run pytest test/test_git_whoami.py   # Single file.
```

## Patterns

- Use the `repo` fixture from `conftest.py` for test isolation.
- Import `TestRepo` from `helper.py` if additional repository setup is needed.

## Configuration isolation

Tests must not modify global or user-level Git configuration. Use `git config --local` only, so all changes are scoped to the temporary test repository created by the `repo` fixture.

## Linting and formatting

```bash
poetry run ruff check test/    # Lint.
poetry run ruff format test/   # Format. Run before committing.
```
