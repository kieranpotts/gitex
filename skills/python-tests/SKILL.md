# Python tests (`test/`)

Tests use pytest with GitPython to create isolated temporary repositories. Every `bin/` script has a matching test file; [`test/test_git_whoami.py`](../../test/test_git_whoami.py) is the canonical example.

## Layout

- `conftest.py` — pytest configuration with shared fixtures (`repo`, `bin`).
- `helper.py` — the `TestRepo` class for creating throwaway Git repositories using GitPython.
- `test_helper.py` — tests for `TestRepo` itself.
- `test_<command>.py` — one test file per Git extension.

## Naming

The mapping between test files and `bin/` scripts is **load-bearing**: the `bin` fixture derives the script path from the test filename by stripping `test_` and replacing each `_` with `-`.

| Test file | Resolved `bin/` script |
| --- | --- |
| `test_git_whoami.py` | `bin/git-whoami` |
| `test_git_push_all.py` | `bin/git-push-all` |
| `test_gitex.py` | `bin/gitex` |

A mismatched filename causes the `bin` fixture to fail with `<script> not found at …`. Test classes use the `Test*` prefix (`python_classes = "Test*"` in [`pyproject.toml`](../../pyproject.toml)), e.g., `TestGitWhoami`.

## Canonical test shape

```python
class TestGitFoo:
    def test_happy_path(self, repo, bin):
        # Arrange: configure the repo as needed.
        repo.git.config("--local", "user.name", "John Doe")

        # Act: run the script-under-test.
        result = repo.run(bin, "--flag")

        # Assert.
        assert result.returncode == 0
        assert "expected" in result.stdout
```

Every test takes the `repo` and `bin` fixtures from [`conftest.py`](../../test/conftest.py):

- `repo` — a fresh `TestRepo` for each test function, already `cd`'d into and configured with a local `user.name` / `user.email`.
- `bin` — the absolute path to the `bin/` script under test, auto-derived from the test filename (see *Naming*).

Cover, at minimum: happy path, error paths, argument validation.

## How scripts are executed

[`TestRepo.run()`](../../test/helper.py) invokes scripts via `subprocess.run(["bash", bin, ...])` — explicitly using `bash`, **not** the script's shebang. This means:

- Tests pass even if the shebang is broken or absent.
- Tests do **not** verify that scripts run correctly when invoked via `PATH` on the user's system.

If you need to test shebang/PATH behavior, do it manually outside pytest.

## Configuration isolation

Tests must not modify global or user-level Git configuration. Use `git config --local` only, so all changes are scoped to the temporary repository created by the `repo` fixture. The fixture sets a minimum `user.name` / `user.email` so tests can make commits without further setup.

`TestRepo` itself is excluded from pytest's collection via a `filterwarnings` rule in [`pyproject.toml`](../../pyproject.toml); this is why a class named `TestRepo` is allowed despite the `Test*` collection pattern.

## Running tests

```bash
poetry install                              # Install dependencies.
poetry run pytest                           # Run the full suite.
poetry run pytest -v                        # Verbose output.
poetry run pytest test/test_git_whoami.py   # Single file.
```

## Linting and formatting

```bash
poetry run ruff check test/    # Lint.
poetry run ruff format test/   # Format. Run before committing.
```
