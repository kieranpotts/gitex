"""
Test suite for git-last command.
"""

# import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def test_script():
    """Get the path to the git-last script"""

    repo_dir = Path(__file__).parent.parent
    script_path = repo_dir / "bin" / "git-last"

    assert script_path.exists(), f"git-last script not found at {script_path}"

    return str(script_path)


class TestGitLast:
    """Test cases for git-last command"""

    # def test_xxxxxxxx(self, temp_repo, test_script):
    #     """Test when ..."""

    #     git = temp_repo.git()
    #     git.config("--local", "user.name", "John Doe")
    #     git.config("--local", "user.email", "john.doe@example.com")

    #     result = subprocess.run(
    #         [test_script], cwd=temp_repo.cwd(), capture_output=True, text=True
    #     )

    #     assert result.returncode == 0
    #     assert "name:  John Doe" in result.stdout
    #     assert "email: john.doe@example.com" in result.stdout
