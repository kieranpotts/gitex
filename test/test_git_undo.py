"""
Test suite for git-undo command.
"""

import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def test_script():
    """Get the path to the git-undo script"""

    repo_dir = Path(__file__).parent.parent
    script_path = repo_dir / "bin" / "git-undo"

    assert script_path.exists(), f"git-undo script not found at {script_path}"

    return str(script_path)


class TestGitUndo:
    """Test cases for git-undo command"""

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
