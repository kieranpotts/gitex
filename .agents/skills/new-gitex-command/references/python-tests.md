# Python tests

Read this before writing or reviewing any file in `test/`.

GitEx's pytest suite runs each `bin/` script as a subprocess against a throwaway
Git repository.

## File and class naming

- A test file for a `bin/` script MUST be named `test_` plus the script name,
  with every `-` turned into `_`. Examples:

  - `test_git_whoami.py` resolves to `bin/git-whoami`.
  - `test_git_push_all.py` resolves to `bin/git-push-all`.
  - `test_gitex.py` resolves to `bin/gitex`.

  A mismatched name fails every test in the file with
  `<script> not found at …`.

- Tests MUST be methods of a class whose name starts with `Test`.

## Fixtures

Tests SHOULD take the two shared fixtures from `test/conftest.py`.

- `repo`. A fresh `TestRepo` (from `test/helper.py`) for each test function.
  It creates a temporary repository, changes into it, and sets a local
  `user.name` and `user.email`.

- `bin`. The absolute path to the script-under-test, derived from the test
  file name.

`TestRepo` wraps a GitPython repository (`repo.git.<command>(…)`) and adds
file helpers — `write`, `read`, `exists`, `remove`, `mkdir`, `path` — and
`run`, which runs the script and returns a `subprocess.CompletedProcess`.

## Test shape

Each test SHOULD follow the **arrange, act, assert** shape, with a comment
marking each part and a docstring saying what it tests.

```python
class TestGitFoo:
    """Test cases for git-foo command."""

    def test_happy_path(self, repo, bin):
        """Test that git-foo prints the last commit message."""

        # Arrange.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Act.
        result = repo.run(bin)

        # Assert.
        assert result.returncode == 0
        assert "initial commit" in result.stdout
```

## Other rules

- A test suite for a command MUST cover at least the happy path, one error
  path, and argument validation. Argument validation includes `--no-color`,
  unknown options, and contradictory or repeated options given in either
  order.

- Tests MUST NOT change global or user-level Git configuration. Use
  `git config --local` only, so that every change stays inside the temporary
  repository.

- An error path SHOULD assert on the exit code and on `result.stderr`, and a
  data result on `result.stdout`, because the scripts send messages and data
  to different streams.

- A test that passes `env=` to `repo.run()` MUST extend the current
  environment rather than replace it, eg. `{**os.environ, "FORCE_COLOR": "1"}`.
  `env=` replaces the whole environment of the subprocess, so a bare dict
  drops `PATH` and `HOME`.

- Tests SHOULD be run through `mise exec`, so that the versions pinned in
  `mise.toml` are used rather than whatever is on `PATH`.

  ```sh
  mise exec -- poetry run pytest test/test_git_<name>.py -v
  mise exec -- poetry run ruff check test/
  ```

## Edge cases

- If a test needs color output, then set `FORCE_COLOR` explicitly through
  `env=`. An autouse fixture, `no_color_env`, clears `NO_COLOR`,
  `GITEX_NO_COLOR`, and `FORCE_COLOR` before every test, so the developer's own
  shell settings never leak in, and the subprocess's stderr is not a terminal.

- Tests cannot catch a broken shebang or a bashism. `TestRepo.run()` always
  runs the script as `bash <script>`, ignoring the shebang. Check that behavior
  by hand, under Dash, outside pytest.

- If pytest warns that it cannot collect the test class `TestRepo`, then the
  `filterwarnings` entry in `pyproject.toml` that suppresses that warning has
  been lost.

- If a test depends on the working directory, then save and restore it
  explicitly. The `repo` fixture changes into the temporary repository, and
  nothing changes back afterwards.

- If the script reads from stdin, eg. at an interactive prompt, then pass the
  answers through `input=`, ending each one with `\n`.
