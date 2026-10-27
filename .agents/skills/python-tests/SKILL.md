---
name: python-tests
description: Conventions and patterns for the pytest suite.
compatibility: requires poetry, python >= 3.12, pytest
license: MIT
---

# Python tests

Use this skill when authoring or modifying a test in `test/`.

Every `bin/` script has a matching `test_<command>.py`.

Tests use pytest with GitPython to create isolated temporary Git repositories.

Do NOT use this skill for editing shell scripts (see [shell-scripts](../shell-scripts/SKILL.md)) or for running the test pipeline (see [testing](../testing/SKILL.md)).

## Rules

-   **Name the file deterministically.**

    The mapping between test files and `bin/` scripts is _load-bearing_. The `bin` fixture strips `test_` and replaces each `_` with `-`. Examples:

    - `test_git_whoami.py` resolves to `bin/git-whoami`
    - `test_git_push_all.py` → `bin/git-push-all`
    - `test_gitex.py` → `bin/gitex`

    A mismatched filename causes the `bin` fixture to fail with `<script> not found at …`.

    Test classes use the `Test*` prefix – see `python_classes = "Test*"` in [`pyproject.toml`](../../pyproject.toml).

-   **Use the shared fixtures.**

    Every test takes `repo` and `bin` from [`test/conftest.py`](../../test/conftest.py):

    - `repo`: A fresh `TestRepo` for each function, already `cd`'d into and configured with a local `user.name` / `user.email`.

    - `bin`: The absolute path to the script under test, auto-derived from the test filename.

-   **Follow the canonical test shape:**

    ```python
    class TestGitFoo:
        def test_happy_path(self, repo, bin):
            # Arrange.
            repo.git.config("--local", "user.name", "John Doe")

            # Act.
            result = repo.run(bin, "--flag")

            # Assert.
            assert result.returncode == 0
            assert "expected" in result.stdout
    ```

    Cover at minimum: happy path, one error path, argument validation.

-   **Keep config isolated.**

    Tests MUST NOT modify global or user-level Git configuration. Use `git config --local` only, so all changes stay inside the temporary repo created by the `repo` fixture.

-   **Lint and format.**

    Run `poetry run ruff check test/` and `poetry run ruff format test/` (or `./fix`) before committing.

-   **`TestRepo.run()` uses `bash`, not the script's shebang**

    See [`test/helper.py`](../../test/helper.py).

    A consequence is that tests will pass even if the shebang is broken or absent. To verify shebang/PATH behavior, do it manually outside pytest.

-   **`TestRepo` is NOT a pytest test class.**

    A `filterwarnings` rule in [`pyproject.toml`](../../pyproject.toml) suppresses the collection warning.

-   **The `repo` fixture `cd`'s into the temp directory.**

    No fixture restores `cwd`, because the `repo` fixture is function scoped anyway.

    If a test relies on the parent directory, save and restore explicitly.

## Examples

Run just a new test:

```sh
poetry run pytest test/test_git_foo.py -v
```

Assert on stderr for an error path:

```python
def test_rejects_unknown_flag(self, repo, bin):
    result = repo.run(bin, "--bogus")

    assert result.returncode == 1
    assert "unknown option" in result.stderr
```
