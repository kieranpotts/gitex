"""
Test suite for git-br command.
"""

import os


class TestGitBr:
    """Test cases for git-br command."""

    # In the test environment, `git push` operations fail because there is not
    # remote to push to. Therefore, `git cl` is expected to return an error.
    # We can't therefore test for a successful operation, but we can at least
    # verify the new branches are created and checked out.

    def test_create_branch_with_argument(self, repo, bin):
        """Test creating a branch with name provided as argument."""

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        repo.run(bin, "feature-branch")

        # Verify the branch was created.
        branches = repo.git.branch()
        assert "feature-branch" in branches

        # Verify we're on the new branch.
        current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD")
        assert current_branch == "feature-branch"

    def test_create_branch_with_stdin(self, repo, bin):
        """Test creating a branch with name provided via stdin."""

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Provide branch name via stdin.
        repo.run(bin, input="my-feature\n")

        # Verify the branch was created.
        branches = repo.git.branch()
        assert "my-feature" in branches

        # Verify we're on the new branch.
        current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD")
        assert current_branch == "my-feature"

    def test_reject_empty_branch_name_from_stdin(self, repo, bin):
        """Test that empty branch name via stdin is rejected."""

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Provide empty branch name via stdin.
        result = repo.run(bin, input="\n")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "Branch name cannot be empty" in result.stderr

    def test_reject_multiple_arguments(self, repo, bin):
        """Test that multiple arguments are rejected."""

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        result = repo.run(bin, "branch1", "branch2")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "git-br accepts at most one argument" in result.stderr

    def test_fail_on_duplicate_branch_name(self, repo, bin):
        """Test that creating a branch with existing name fails."""

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Create a branch.
        repo.git.branch("existing-branch")

        # Try to create the same branch again.
        result = repo.run(bin, "existing-branch")

        # Verify error exit code.
        assert result.returncode != 0

        # Verify git error about existing branch.
        assert "already exists" in result.stderr or "fatal" in result.stderr

    def test_branch_from_specific_commit(self, repo, bin):
        """Test that new branch is created from current HEAD position."""

        # Create multiple commits.
        repo.write("file1.txt", "Content 1")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "commit 1")

        repo.write("file2.txt", "Content 2")
        repo.git.add("file2.txt")
        repo.git.commit("-m", "commit 2")

        # Get current commit hash.
        original_commit = repo.git.rev_parse("HEAD")

        # Create new branch.
        repo.run(bin, "new-branch")

        # Verify the new branch points to the same commit.
        new_branch_commit = repo.git.rev_parse("HEAD")
        assert new_branch_commit == original_commit

    def test_custom_remote_via_environment_variable(self, repo, bin):
        """Test using custom remote name via X_GITEX_DEFAULT_REMOTE_NAME."""

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Set custom remote name via environment variable.
        env = os.environ.copy()
        env["X_GITEX_DEFAULT_REMOTE_NAME"] = "upstream"

        # Run with custom environment.
        result = repo.run(bin, "custom-remote-branch", env=env)

        # Verify the branch was created.
        branches = repo.git.branch()
        assert "custom-remote-branch" in branches

        # Verify we're on the new branch.
        current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD")
        assert current_branch == "custom-remote-branch"

        # Verify the error message mentions the custom remote name.
        # Since there's no actual remote, the push will fail, but
        # at least we can inspect the error message to verify Git
        # stried to push to the remote we expect.
        assert "upstream" in result.stderr

    def test_default_remote_when_env_var_empty(self, repo, bin):
        """Test that empty environment variable falls back to 'origin'."""

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Set empty remote name via environment variable.
        env = os.environ.copy()
        env["X_GITEX_DEFAULT_REMOTE_NAME"] = ""

        # Run with custom environment.
        result = repo.run(bin, "default-remote-branch", env=env)

        # Verify the branch was created.
        branches = repo.git.branch()
        assert "default-remote-branch" in branches

        # Verify the error message mentions 'origin' (the default).
        assert "origin" in result.stderr
