# Sharing fixtures
# Ref: https://docs.pytest.org/en/6.2.x/fixture.html#scope-sharing-fixtures-across-classes-modules-packages-or-session

from pathlib import Path

import pytest

from helper import TestRepo


@pytest.fixture(scope="function")
def test_repo():
    """
    Create a temporary Git repository that is reset for each test
    function call.
    """

    test_repo = TestRepo()

    test_repo.git.config("--local", "user.name", "John Doe")
    test_repo.git.config("--local", "user.email", "john.doe@example.com")

    return test_repo


@pytest.fixture
def script_path(request):
    """
    Get the path to a git extension script based on the test file name.
    Automatically derives the script name from the test file name.
    """

    # Get the test file name (eg. 'test_git_whoami.py').
    test_file = Path(request.fspath)

    # Extract script name from test file name,
    # eg. 'test_git_whoami.py' -> 'git-whoami'.
    script_name = test_file.stem.replace("test_", "").replace("_", "-")

    # Get the repo directory - resolve symlinks to ensure we get the real path.
    repo_dir = test_file.parent.parent.resolve()
    script_path = repo_dir / "bin" / script_name

    assert script_path.exists(), f"{script_name} script not found at {script_path}"
    assert script_path.is_file(), f"{script_path} exists but is not a file"

    # Ensure the script is executable.
    script_path.chmod(0o755)

    return str(script_path)
