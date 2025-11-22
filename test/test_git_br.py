"""
Test suite for git-br command.
"""

import os
from pathlib import Path


class TestGitBr:
    """Test cases for git-br command."""

    # In the test environment, `git push` operations fail because there is not
    # remote to push to. Therefore, `git cl` is expected to return an error.
    # We can't therefore test for a successful operation, but we can at least
    # verify the new branches are created and checked out.

    def test_create_branch_with_argument(self, temp_repo, script_path):
        """Test creating a branch with name provided as argument."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "Initial commit")

        temp_repo.run(script_path, "feature-branch")

        # Verify the branch was created.
        branches = git.branch()
        assert "feature-branch" in branches

        # Verify we're on the new branch.
        current_branch = git.rev_parse("--abbrev-ref", "HEAD")
        assert current_branch == "feature-branch"

    def test_create_branch_with_stdin(self, temp_repo, script_path):
        """Test creating a branch with name provided via stdin."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "Initial commit")

        # Provide branch name via stdin.
        temp_repo.run(script_path, input="my-feature\n")

        # Verify the branch was created.
        branches = git.branch()
        assert "my-feature" in branches

        # Verify we're on the new branch.
        current_branch = git.rev_parse("--abbrev-ref", "HEAD")
        assert current_branch == "my-feature"

    def test_reject_empty_branch_name_from_stdin(self, temp_repo, script_path):
        """Test that empty branch name via stdin is rejected."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "Initial commit")

        # Provide empty branch name via stdin.
        result = temp_repo.run(script_path, input="\n")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "Branch name cannot be empty" in result.stderr

    def test_reject_multiple_arguments(self, temp_repo, script_path):
        """Test that multiple arguments are rejected."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "Initial commit")

        result = temp_repo.run(script_path, "branch1", "branch2")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "git-br accepts at most one argument" in result.stderr

    def test_fail_on_duplicate_branch_name(self, temp_repo, script_path):
        """Test that creating a branch with existing name fails."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "Initial commit")

        # Create a branch.
        git.branch("existing-branch")

        # Try to create the same branch again.
        result = temp_repo.run(script_path, "existing-branch")

        # Verify error exit code.
        assert result.returncode != 0

        # Verify git error about existing branch.
        assert "already exists" in result.stderr or "fatal" in result.stderr

    def test_branch_from_specific_commit(self, temp_repo, script_path):
        """Test that new branch is created from current HEAD position."""

        git = temp_repo.git()

        # Create multiple commits.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content 1")
        git.add("file1.txt")
        git.commit("-m", "Commit 1")

        Path(temp_repo.cwd(), "file2.txt").write_text("Content 2")
        git.add("file2.txt")
        git.commit("-m", "Commit 2")

        # Get current commit hash.
        original_commit = git.rev_parse("HEAD")

        # Create new branch.
        temp_repo.run(script_path, "new-branch")

        # Verify the new branch points to the same commit.
        new_branch_commit = git.rev_parse("HEAD")
        assert new_branch_commit == original_commit

    def test_custom_remote_via_environment_variable(self, temp_repo, script_path):
        """Test using custom remote name via X_GITEX_DEFAULT_REMOTE_NAME."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "Initial commit")

        # Set custom remote name via environment variable.
        env = os.environ.copy()
        env["X_GITEX_DEFAULT_REMOTE_NAME"] = "upstream"

        # Run with custom environment.
        import subprocess

        result = subprocess.run(
            ["bash", script_path, "custom-remote-branch"],
            cwd=temp_repo.cwd(),
            capture_output=True,
            text=True,
            env=env,
        )

        # Verify the branch was created.
        branches = git.branch()
        assert "custom-remote-branch" in branches

        # Verify we're on the new branch.
        current_branch = git.rev_parse("--abbrev-ref", "HEAD")
        assert current_branch == "custom-remote-branch"

        # Verify the error message mentions the custom remote name.
        # Since there's no actual remote, the push will fail, but
        # at least we can inspect the error message to verify Git
        # stried to push to the remote we expect.
        assert "upstream" in result.stderr

    def test_default_remote_when_env_var_empty(self, temp_repo, script_path):
        """Test that empty environment variable falls back to 'origin'."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "Initial commit")

        # Set empty remote name via environment variable.
        env = os.environ.copy()
        env["X_GITEX_DEFAULT_REMOTE_NAME"] = ""

        # Run with custom environment.
        import subprocess

        result = subprocess.run(
            ["bash", script_path, "default-remote-branch"],
            cwd=temp_repo.cwd(),
            capture_output=True,
            text=True,
            env=env,
        )

        # Verify the branch was created.
        branches = git.branch()
        assert "default-remote-branch" in branches

        # Verify the error message mentions 'origin' (the default).
        assert "origin" in result.stderr
