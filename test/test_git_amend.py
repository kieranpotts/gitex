"""
Test suite for git-amend command.
"""

import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def test_script():
    """Get the path to the git-amend script."""

    repo_dir = Path(__file__).parent.parent
    script_path = repo_dir / "bin" / "git-amend"

    assert script_path.exists(), f"git-amend script not found at {script_path}"

    return str(script_path)


class TestGitAmend:
    """Test cases for git-amend command."""

    def test_amend_with_unstaged_changes(self, temp_repo, test_script):
        """Test amending with unstaged changes."""

        git = temp_repo.git()
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "initial commit")

        # Make unstaged changes.
        Path(temp_repo.cwd(), "file1.txt").write_text("Modified content")

        # Run git-amend.
        result = subprocess.run(
            [test_script], cwd=temp_repo.cwd(), capture_output=True, text=True
        )

        assert result.returncode == 0

        # Verify there's still only one commit.
        log_output = git.log("--oneline")
        assert log_output.count("\n") == 0

        # Verify the file content in the commit.
        show_output = git.show("HEAD:file1.txt")
        assert "Modified content" in show_output

        # Verify commit message unchanged.
        commit_msg = git.log("-1", "--format=%s")
        assert commit_msg == "initial commit"

    def test_amend_with_untracked_files(self, temp_repo, test_script):
        """Test amending with new untracked files."""

        git = temp_repo.git()
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "first commit")

        # Create untracked file.
        Path(temp_repo.cwd(), "file2.txt").write_text("New file")

        # Run git-amend.
        result = subprocess.run(
            [test_script], cwd=temp_repo.cwd(), capture_output=True, text=True
        )

        assert result.returncode == 0

        # Verify the new file was added to the commit.
        ls_tree = git.ls_tree("-r", "--name-only", "HEAD")
        assert "file1.txt" in ls_tree
        assert "file2.txt" in ls_tree

        # Verify still only one commit.
        log_output = git.log("--oneline")
        assert log_output.count("\n") == 0

    def test_amend_with_staged_changes(self, temp_repo, test_script):
        """Test amending with already staged changes."""

        git = temp_repo.git()
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "initial commit")

        # Make and stage changes.
        Path(temp_repo.cwd(), "file1.txt").write_text("Staged content")
        git.add("file1.txt")

        # Run git-amend.
        result = subprocess.run(
            [test_script], cwd=temp_repo.cwd(), capture_output=True, text=True
        )

        assert result.returncode == 0

        # Verify the changes were added to the last commit.
        show_output = git.show("HEAD:file1.txt")
        assert "Staged content" in show_output

    def test_amend_with_mixed_changes(self, temp_repo, test_script):
        """Test amending with staged, unstaged, and untracked files."""

        git = temp_repo.git()
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content 1")
        Path(temp_repo.cwd(), "file2.txt").write_text("Content 2")
        git.add(".")
        git.commit("-m", "initial commit")

        # Staged change.
        Path(temp_repo.cwd(), "file1.txt").write_text("Staged content")
        git.add("file1.txt")

        # Unstaged change.
        Path(temp_repo.cwd(), "file2.txt").write_text("Unstaged content")

        # Untracked file.
        Path(temp_repo.cwd(), "file3.txt").write_text("New file")

        # Run git-amend.
        result = subprocess.run(
            [test_script], cwd=temp_repo.cwd(), capture_output=True, text=True
        )

        assert result.returncode == 0

        # Verify all changes were included.
        assert "Staged content" in git.show("HEAD:file1.txt")
        assert "Unstaged content" in git.show("HEAD:file2.txt")
        assert "New file" in git.show("HEAD:file3.txt")

        # Verify still only one commit.
        log_output = git.log("--oneline")
        assert log_output.count("\n") == 0

    def test_error_no_commits_exist(self, temp_repo, test_script):
        """Test error when there are no commits to amend."""

        git = temp_repo.git()
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        # Create a file but don't commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content")

        # Run git-amend.
        result = subprocess.run(
            [test_script], cwd=temp_repo.cwd(), capture_output=True, text=True
        )

        assert result.returncode == 1
        assert "error: no commits exist to amend" in result.stderr

    def test_rejects_single_argument(self, temp_repo, test_script):
        """Test that the command rejects arguments."""

        git = temp_repo.git()
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content")
        git.add("file1.txt")
        git.commit("-m", "initial commit")

        result = subprocess.run(
            [test_script, "--help"], cwd=temp_repo.cwd(), capture_output=True, text=True
        )

        assert result.returncode == 1
        assert "error: git-amend does not accept any arguments" in result.stderr

    def test_rejects_multiple_arguments(self, temp_repo, test_script):
        """Test that the command rejects multiple arguments."""

        git = temp_repo.git()
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content")
        git.add("file1.txt")
        git.commit("-m", "initial commit")

        result = subprocess.run(
            [test_script, "arg1", "arg2"],
            cwd=temp_repo.cwd(),
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert "error: git-amend does not accept any arguments" in result.stderr

    def test_commit_message_preserved(self, temp_repo, test_script):
        """Test that the commit message is preserved when amending."""

        git = temp_repo.git()
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        # Create initial commit with specific message.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content")
        git.add("file1.txt")
        git.commit("-m", "my custom commit message")

        # Make changes.
        Path(temp_repo.cwd(), "file1.txt").write_text("Modified")

        # Run git-amend.
        result = subprocess.run(
            [test_script], cwd=temp_repo.cwd(), capture_output=True, text=True
        )

        assert result.returncode == 0

        # Verify commit message is unchanged.
        commit_msg = git.log("-1", "--format=%s")
        assert commit_msg == "my custom commit message"
