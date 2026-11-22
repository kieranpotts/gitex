# Running checks

Read this before running `./run/fix` or `./run/check`, or when diagnosing a
failure from either. Both scripts run against the working tree from the
repository root.

## Toolchain

Check the toolchain is installed before running anything.

```sh
mise exec -- poetry run pytest --version
```

If that fails, stop, and ask the user to run `./run/install`.

## The pipelines

- `./run/fix` runs Ruff's formatter over `test/`. There is no auto-fixer for
  shell scripts. Run it before `./run/check` whenever any file in `test/` has
  changed.

- `./run/check` runs three stages in order, and stops at the first failure.

  1. ShellCheck on `bin/*` and `lib/*`, at style severity.
  2. Ruff lint on `test/`.
  3. pytest on `test/`, verbose.

For a quicker loop while working on one script or test file, run the matching
stage directly, then finish with a full `./run/check`.

```sh
mise exec -- shellcheck --severity=style bin/git-<name>
mise exec -- poetry run pytest test/test_git_<name>.py -v
```

## Diagnosing failures

Pin each failure down to its stage (ShellCheck, Ruff, or pytest), its file and
line, and the ShellCheck code, Ruff rule, or pytest test ID.

- For a ShellCheck finding, read the flagged line and look up the code's
  meaning.

- For a pytest failure, read the assertion, the captured stdout and stderr, and
  the script under test, and decide whether the script or the test is wrong.

## Rules

- You SHOULD run the `run/` scripts rather than the tools they wrap. They pin
  the working directory and the tool versions, which is what CI runs.

- A tool run directly MUST go through `mise exec --`, so that the versions
  pinned in `mise.toml` are used rather than whatever is on `PATH`.

- You MUST NOT run `./run/install` yourself. It changes the machine's toolchain.
  The user runs it by hand, including in the workspace devcontainer.

- You MUST NOT make a check pass by weakening it, eg. by adding a
  `# shellcheck disable` directive, a `# noqa` comment, or a skip marker.

## Edge cases

- If pytest fails only on the host or only in the devcontainer, then compare
  the two environments' Git versions and Git configuration. The tests set a
  local `user.name` and `user.email`, but other global settings, such as
  `init.defaultBranch`, still reach them through the devcontainer.

- If a script passes every stage but fails when run as `git <name>`, then
  suspect a shebang or bashism fault. pytest runs every script with
  `bash <script>`, ignoring the shebang, so neither can fail in the suite.

- `./run/check` does not check commit messages. They are validated only in CI,
  by the `validate-commit-messages.yaml` workflow.
