"""
Test suite for git-whoami command.
"""

import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def test_script():
    """Get the path to the git-whoami script"""

    repo_dir = Path(__file__).parent.parent
    script_path = repo_dir / "bin" / "git-whoami"

    assert script_path.exists(), f"git-whoami script not found at {script_path}"

    return str(script_path)


class TestGitWhoami:
    """Test cases for git-whoami command"""

    def test_with_name_and_email_set(self, temp_repo, test_script):
        """Test when both user.name and user.email are configured"""

        git = temp_repo.git()
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        result = subprocess.run(
            [test_script], cwd=temp_repo.cwd(), capture_output=True, text=True
        )

        assert result.returncode == 0
        assert "name:  John Doe" in result.stdout
        assert "email: john.doe@example.com" in result.stdout

    def test_with_neither_name_nor_email_set(self, temp_repo, test_script):
        """Test when neither user.name nor user.email are configured"""

        git = temp_repo.git()
        git.config("--local", "user.name", "")
        git.config("--local", "user.email", "")

        result = subprocess.run(
            [test_script], cwd=temp_repo.cwd(), capture_output=True, text=True
        )

        assert result.returncode == 0
        assert "name:  [not set]" in result.stdout
        assert "email: [not set]" in result.stdout

    def test_with_only_name_set(self, temp_repo, test_script):
        """Test when only user.name is configured"""

        git = temp_repo.git()
        git.config("--local", "user.name", "Jane Doe")
        git.config("--local", "user.email", "")

        result = subprocess.run(
            [test_script], cwd=temp_repo.cwd(), capture_output=True, text=True
        )

        assert result.returncode == 0
        assert "name:  Jane Doe" in result.stdout
        assert "email: [not set]" in result.stdout

    def test_with_only_email_set(self, temp_repo, test_script):
        """Test when only user.email is configured"""

        git = temp_repo.git()
        git.config("--local", "user.name", "")
        git.config("--local", "user.email", "jane.doe@example.com")

        result = subprocess.run(
            [test_script], cwd=temp_repo.cwd(), capture_output=True, text=True
        )

        assert result.returncode == 0
        assert "name:  [not set]" in result.stdout
        assert "email: jane.doe@example.com" in result.stdout

    def test_output_format(self, temp_repo, test_script):
        """Test that the output follows the expected format"""

        git = temp_repo.git()
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        result = subprocess.run(
            [test_script], cwd=temp_repo.cwd(), capture_output=True, text=True
        )

        lines = result.stdout.strip().split("\n")
        assert len(lines) == 2
        assert lines[0].startswith("name:  ")
        assert lines[1].startswith("email: ")

    def test_with_special_characters_in_name(self, temp_repo, test_script):
        """Test with special characters in user name"""

        git = temp_repo.git()
        git.config("--local", "user.name", "José García-Pérez")
        git.config("--local", "user.email", "jose@example.com")

        result = subprocess.run(
            [test_script], cwd=temp_repo.cwd(), capture_output=True, text=True
        )

        assert result.returncode == 0
        assert "name:  José García-Pérez" in result.stdout
        assert "email: jose@example.com" in result.stdout

    def test_rejects_single_argument(self, temp_repo, test_script):
        """Test that the command rejects arguments"""

        result = subprocess.run(
            [test_script, "--help"], cwd=temp_repo.cwd(), capture_output=True, text=True
        )

        assert result.returncode == 1
        assert "error: git-whoami does not accept any arguments" in result.stderr

    def test_rejects_multiple_arguments(self, temp_repo, test_script):
        """Test that the command rejects multiple arguments"""

        result = subprocess.run(
            [test_script, "arg1", "arg2"],
            cwd=temp_repo.cwd(),
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert "error: git-whoami does not accept any arguments" in result.stderr
